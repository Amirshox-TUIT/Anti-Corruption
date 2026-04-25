from typing import Dict

from .types import MessageTemplate

ACCOUNT_MESSAGES: Dict[str, MessageTemplate] = {
    "LOGIN_SUCCESS": {
        "id": "LOGIN_SUCCESS",
        "chats": {
            "en": "Successfully logged in",
            "uz": "Muvaffaqiyatli tizimga kirdingiz",
            "ru": "Вы успешно вошли в систему",
        },
        "status_code": 200
    },

    "LOGIN_FAILED": {
        "id": "LOGIN_FAILED",
        "chats": {
            "en": "Invalid username or password",
            "uz": "Login yoki parol noto‘g‘ri",
            "ru": "Неверный логин или пароль",
        },
        "status_code": 400
    },

    "USER_CREATED": {
        "id": "USER_CREATED",
        "chats": {
            "en": "User account created successfully",
            "uz": "Foydalanuvchi hisobi muvaffaqiyatli yaratildi",
            "ru": "Учетная запись пользователя успешно создана",
        },
        "status_code": 201
    },
    "USER_NOT_FOUND": {
        "id": "USER_NOT_FOUND",
        "chats": {
            "en": "User with ID {user_id} not found",
            "uz": "ID {user_id} bo'lgan foydalanuvchi topilmadi",
            "ru": "Пользователь с ID {user_id} не найден",
        },
        "status_code": 404
    },
    "USER_ALREADY_EXISTS": {
        "id": "USER_ALREADY_EXISTS",
        "chats": {
            "en": "User with email  already exists",
            "uz": "elektron pochtasi bilan foydalanuvchi allaqachon mavjud",
            "ru": "Пользователь с email {email} уже существует",
        },
        "status_code": 400
    },
    "PHONE_EXISTS": {
        "id": "PHONE_EXISTS",
        "chats": {
            "en": "User with phone {phone} already exists",
            "uz": "{phone} elektron pochtasi bilan foydalanuvchi allaqachon mavjud",
            "ru": "Пользователь с phone {phone} уже существует",
        },
        "status_code": 400
    },
    "INVALID_CREDENTIALS": {
        "id": "INVALID_CREDENTIALS",
        "chats": {
            "en": "Invalid email or password",
            "uz": "Noto'g'ri elektron pochta yoki parol",
            "ru": "Неверный email или пароль",
        },
        "status_code": 401
    },
    "ACCOUNT_DISABLED": {
        "id": "ACCOUNT_DISABLED",
        "chats": {
            "en": "Your account has been disabled",
            "uz": "Sizning hisobingiz o'chirilgan",
            "ru": "Ваша учетная запись была отключена",
        },
        "status_code": 403
    },
    "SEARCH_QUERY_REQUIRED": {
        "id": "SEARCH_QUERY_REQUIRED",
        "chats": {
            "en": "Search query is required",
            "uz": "Qidiruv so‘rovi talab qilinadi",
            "ru": "Требуется поисковый запрос"
        },
        "status_code": 400
    },
    "USERS_FOUND": {
        "id": "USERS_FOUND",
        "chats": {
            "en": "Users successfully found",
            "uz": "Foydalanuvchilar muvaffaqiyatli topildi",
            "ru": "Пользователи успешно найдены"
        },
        "status_code": 200
    },
    "AUTHENTICATION_FAILED": {
        "id": "AUTHENTICATION_FAILED",
        "chats": {
            "en": "Authentication failed",
            "uz": "Autentifikatsiya muvaffaqiyatsiz",
            "ru": "Ошибка аутентификации",
        },
        "status_code": 401
    },
    "USER_FOUND": {
        "id": "USER_FOUND",
        "chats": {
            "en": "Users found successfully",
            "uz": "Foydalanuvchilar muvaffaqiyatli topildi",
            "ru": "Пользователи успешно найдены",
        },
        "status_code": 200
    },
    "EMAIL_VERIFICATION_SENT": {
        "id": "EMAIL_VERIFICATION_SENT",
        "chats": {
            "en": "Verification email sent to {email}",
            "uz": "Tasdiqlash emaili {email} ga yuborildi",
            "ru": "Письмо с подтверждением отправлено на {email}",
        },
        "status_code": 200
    },
    "EMAIL_VERIFIED": {
        "id": "EMAIL_VERIFIED",
        "chats": {
            "en": "Email verified successfully",
            "uz": "Email muvaffaqiyatli tasdiqlandi",
            "ru": "Email успешно подтвержден",
        },
        "status_code": 200
    },
    "INVALID_TOKEN": {
        "id": "INVALID_TOKEN",
        "chats": {
            "en": "Invalid or expired token",
            "uz": "Noto'g'ri yoki muddati o'tgan token",
            "ru": "Недействительный или истекший токен",
        },
        "status_code": 400
    },
    "PASSWORD_CHANGED": {
        "id": "PASSWORD_CHANGED",
        "chats": {
            "en": "Password changed successfully",
            "uz": "Parol muvaffaqiyatli o'zgartirildi",
            "ru": "Пароль успешно изменен",
        },
        "status_code": 200
    },
    "PASSWORD_RESET_SENT": {
        "id": "PASSWORD_RESET_SENT",
        "chats": {
            "en": "Password reset instructions sent to your email",
            "uz": "Parolni tiklash bo'yicha ko'rsatmalar emailingizga yuborildi",
            "ru": "Инструкции по сбросу пароля отправлены на ваш email",
        },
        "status_code": 200
    },
    "CODE_NOT_FOUND": {
        "id": "CODE_NOT_FOUND",
        "chats": {
            "en": "Verification code not found for {phone}",
            "uz": "{phone} uchun tasdiqlash kodi topilmadi",
            "ru": "Код подтверждения для {phone} не найден",
        },
        "status_code": 400
    },
    "CODE_EXPIRED": {
        "id": "CODE_EXPIRED",
        "chats": {
            "en": "Verification code for {phone} has expired",
            "uz": "{phone} uchun tasdiqlash kodi muddati tugagan",
            "ru": "Срок действия кода подтверждения для {phone} истек",
        },
        "status_code": 400
    },
    "TOO_MANY_ATTEMPTS": {
        "id": "TOO_MANY_ATTEMPTS",
        "chats": {
            "en": "Too many invalid attempts for {phone}. Try again later",
            "uz": "{phone} uchun juda ko'p noto‘g‘ri urinishlar. Keyinroq urinib ko‘ring",
            "ru": "Слишком много неверных попыток для {phone}. Попробуйте позже",
        },
        "status_code": 429
    },
    "INVALID_CODE": {
        "id": "INVALID_CODE",
        "chats": {
            "en": "Invalid verification code. Remaining attempts: {remaining_attempts}",
            "uz": "Noto‘g‘ri tasdiqlash kodi. Qolgan urinishlar soni: {remaining_attempts}",
            "ru": "Неверный код подтверждения. Осталось попыток: {remaining_attempts}",
        },
        "status_code": 400
    },
    "PHONE_VERIFIED": {
        "id": "PHONE_VERIFIED",
        "chats": {
            "en": "Phone verified successfully",
            "uz": "Telefon muvaffaqiyatli tasdiqlandi",
            "ru": "Телефон успешно подтвержден",
        },
        "status_code": 200
    },
    "OTP_SENT": {
        "id": "OTP_SENT",
        "chats": {
            "en": "Verification code sent successfully",
            "uz": "Tasdiqlash kodi muvaffaqiyatli yuborildi",
            "ru": "Код подтверждения успешно отправлен",
        },
        "status_code": 200
    },
    "TOKEN_IS_NOT_PROVIDED": {
        "id": "TOKEN_IS_NOT_PROVIDED",
        "chats": {
            "en": "Authorization token is not provided",
            "uz": "Avtorizatsiya tokeni taqdim etilmagan",
            "ru": "Токен авторизации не предоставлен"
        },
        "status_code": 401
    },
    "LOGOUT_SUCCESS": {
        "id": "LOGOUT_SUCCESS",
        "chats": {
            "en": "Logout successful",
            "uz": "Chiqish muvaffaqiyatli",
            "ru": "Выход выполнен успешно"
        },
        "status_code": 200
    },
    "LOGOUT_FAILED": {
        "id": "LOGOUT_FAILED",
        "chats": {
            "en": "Logout failed",
            "uz": "Chiqish bajarilmadi",
            "ru": "Не удалось выйти"
        },
        "status_code": 400
    },
}
