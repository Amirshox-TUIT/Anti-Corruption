import json
import os
from dataclasses import dataclass

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency at runtime
    OpenAI = None


@dataclass
class AIInsight:
    summary: str
    risk_score: int
    flags: list[str]
    source: str


KEYWORD_FLAGS = {
    "bribe": "bribery_signal",
    "payment": "offbook_payment_signal",
    "cash": "cash_demand_signal",
    "kickback": "kickback_signal",
    "procurement": "procurement_signal",
    "supplier": "supplier_bias_signal",
    "license": "licensing_pressure_signal",
    "threat": "coercion_signal",
    "delay": "artificial_delay_signal",
}


def _fallback_insight(description: str, corruption_type: str) -> AIInsight:
    lower_text = description.lower()
    flags = [flag for keyword, flag in KEYWORD_FLAGS.items() if keyword in lower_text]

    base_scores = {
        "bribery": 74,
        "embezzlement": 82,
        "abuse-of-power": 76,
        "procurement": 80,
        "extortion": 88,
        "other": 62,
    }
    score = base_scores.get(corruption_type, 62) + min(len(flags) * 2, 10)
    score = max(1, min(score, 99))

    summary = (
        "The report was auto-profiled for triage. "
        f"Type={corruption_type}, indicators={len(flags)}."
    )
    return AIInsight(summary=summary, risk_score=score, flags=flags[:8], source="heuristic")


def _openai_insight(description: str, corruption_type: str) -> AIInsight | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or not OpenAI:
        return None

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    prompt = (
        "Return strict JSON only with keys: summary, risk_score, flags.\n"
        "risk_score must be integer 1..99.\n"
        "flags must be a JSON array of short snake_case strings.\n"
        f"corruption_type: {corruption_type}\n"
        f"description: {description}\n"
    )

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    output = (response.output_text or "").strip()
    if not output:
        return None

    parsed = json.loads(output)
    summary = str(parsed.get("summary", "")).strip()
    risk_score = int(parsed.get("risk_score", 65))
    risk_score = max(1, min(risk_score, 99))
    flags = parsed.get("flags", [])
    if not isinstance(flags, list):
        flags = []
    normalized_flags = [str(item).strip().replace(" ", "_") for item in flags if str(item).strip()]

    if not summary:
        return None

    return AIInsight(
        summary=summary,
        risk_score=risk_score,
        flags=normalized_flags[:8],
        source="openai",
    )


def build_report_ai_insight(description: str, corruption_type: str) -> AIInsight:
    try:
        insight = _openai_insight(description=description, corruption_type=corruption_type)
        if insight:
            return insight
    except Exception:
        pass

    return _fallback_insight(description=description, corruption_type=corruption_type)
