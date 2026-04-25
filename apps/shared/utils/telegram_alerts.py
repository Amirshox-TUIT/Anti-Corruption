import html
import logging
import threading

try:
    import telebot
except Exception:  # pragma: no cover - optional dependency
    telebot = None

from apps.shared.utils.custom_current_host import get_client_ip
from core import config

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN) if (telebot and config.TELEGRAM_BOT_TOKEN) else None


def _send_telegram_message(text: str):
    """Internal function: Sends a Telegram message (runs inside thread)."""
    if not bot or not config.TELEGRAM_CHANNEL_ID:
        return

    try:
        bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error("Failed to send alert to Telegram: %s", e)


def send_alert(text: str):
    """Starts a thread to send alert without blocking."""
    threading.Thread(target=_send_telegram_message, args=(text,), daemon=True).start()


def alert_to_telegram(traceback_text: str, message: str = "No message provided",
                      request=None, ip: str = None,
                      port: str = None):
    if not isinstance(message, str):
        message = str(message)

    if request and not ip:
        ip = get_client_ip(request)
        port = request.META.get("REMOTE_PORT")

    safe_message = html.escape(message)
    safe_traceback = html.escape(traceback_text)
    safe_ip = html.escape(ip) if ip else "unknown"
    safe_port = html.escape(str(port)) if port else "unknown"

    text = (
        "❌ <b>Exception Alert</b> ❌\n\n"
        f"<b>✍️ Message:</b> <code>{safe_message}</code>\n\n"
        f"<b>🔖 Traceback:</b> <code>{safe_traceback}</code>\n\n"
        f"<b>🌐 IP Address/Port:</b> <code>{safe_ip}:{safe_port}</code>\n\n"
    )
    send_alert(text)
