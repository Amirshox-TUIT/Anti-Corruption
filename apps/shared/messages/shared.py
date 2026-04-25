from typing import Dict

from .types import MessageTemplate

SHARED_MESSAGES: Dict[str, MessageTemplate] = {
    "SUCCESS_MESSAGE": {
        "id": "SUCCESS_MESSAGE",
        "chats": {
            "en": "Operation completed successfully",
            "uz": "Operatsiya muvaffaqiyatli yakunlandi",
            "ru": "Операция успешно завершена",
        },
        "status_code": 200
    },
    "CREATED": {
        "id": "CREATED",
        "chats": {
            "en": "Resource created successfully",
            "uz": "Resurs muvaffaqiyatli yaratildi",
            "ru": "Ресурс успешно создан",
        },
        "status_code": 201
    },
    "NOT_CREATED": {
        "id": "NOT_CREATED",
        "chats": {
            "en": "Resource not created successfully",
            "uz": "Resurs muvaffaqiyatli yaratilmadi",
            "ru": "Ресурс не создан успешно",
        },
        "status_code": 500
    },
    "UPDATED": {
        "id": "UPDATED",
        "chats": {
            "en": "Resource updated successfully",
            "uz": "Resurs muvaffaqiyatli yangilandi",
            "ru": "Ресурс успешно обновлен",
        },
        "status_code": 200
    },
    "NOT_UPDATED": {
        "id": "NOT_UPDATED",
        "chats": {
            "en": "Resource does not updated successfully",
            "uz": "Resurs muvaffaqiyatli yangilanmadi",
            "ru": "Ресурс не обновлен успешно",
        },
        "status_code": 500
    },
    "DELETED": {
        "id": "DELETED",
        "chats": {
            "en": "Resource deleted successfully",
            "uz": "Resurs muvaffaqiyatli o'chirildi",
            "ru": "Ресурс успешно удален",
        },
        "status_code": 200
    },
    "VALIDATION_ERROR": {
        "id": "VALIDATION_ERROR",
        "chats": {
            "en": "Invalid input data",
            "uz": "Noto'g'ri ma'lumot kiritildi",
            "ru": "Неверные входные данные",
        },
        "status_code": 400
    },
    "NOT_FOUND": {
        "id": "NOT_FOUND",
        "chats": {
            "en": "Resource not found",
            "uz": "Resurs topilmadi",
            "ru": "Ресурс не найден",
        },
        "status_code": 404
    },
    "PERMISSION_DENIED": {
        "id": "PERMISSION_DENIED",
        "chats": {
            "en": "You don't have permission to perform this action",
            "uz": "Sizda bu amalni bajarish uchun ruxsat yo'q",
            "ru": "У вас нет прав для выполнения этого действия",
        },
        "status_code": 403
    },
    "UNAUTHORIZED": {
        "id": "UNAUTHORIZED",
        "chats": {
            "en": "Authentication required",
            "uz": "Autentifikatsiya talab qilinadi",
            "ru": "Требуется аутентификация",
        },
        "status_code": 401
    },
    "INTERNAL_SERVER_ERROR": {
        "id": "INTERNAL_SERVER_ERROR",
        "chats": {
            "en": "Internal server error occurred",
            "uz": "Ichki server xatosi yuz berdi",
            "ru": "Произошла внутренняя ошибка сервера",
        },
        "status_code": 500
    },
    "UNKNOWN_ERROR": {
        "id": "UNKNOWN_ERROR",
        "chats": {
            "en": "An unexpected error occurred",
            "uz": "Kutilmagan xatolik yuz berdi",
            "ru": "Произошла непредвиденная ошибка",
        },
        "status_code": 500
    },
    "SYSTEM_ERROR": {
        "id": "SYSTEM_ERROR",
        "chats": {
            "en": "System error occurred",
            "uz": "Tizim xatosi yuz berdi",
            "ru": "Произошла системная ошибка",
        },
        "status_code": 500
    },
    "POST_CREATED": {
        "id": "POST_CREATED",
        "chats": {
            "en": "Post created successfully",
            "uz": "Post muvaffaqiyatli yaratildi",
            "ru": "Пост успешно создан",
        },
        "status_code": 201
    },
    "POSTS_FETCHED": {
        "id": "POSTS_FETCHED",
        "chats": {
            "en": "Posts fetched successfully",
            "uz": "Postlar muvaffaqiyatli olib kelindi",
            "ru": "Посты успешно получены"
        },
        "status_code": 200
    },
    "FOLLOWINGS_FETCHED": {
        "id": "FOLLOWINGS_FETCHED",
        "chats": {
            "en": "Followings fetched successfully",
            "uz": "Kuzatuvlar muvaffaqiyatli olib kelindi",
            "ru": "Список подписок успешно получен"
        },
        "status_code": 200
    },
    "FOLLOWERS_FETCHED": {
            "id": "FOLLOWERS_FETCHED",
            "chats": {
                "en": "Followers fetched successfully",
                "uz": "Kuzatuvlarchilar muvaffaqiyatli olib kelindi",
                "ru": "Список подписчиков успешно получен"
            },
            "status_code": 200
        },
    "NO_MORE_POSTS": {
        "id": "NO_MORE_POSTS",
        "chats": {
            "en": "No more posts available",
            "uz": "Boshqa postlar mavjud emas",
            "ru": "Больше постов нет"
        },
        "status_code": 204
    },

}
