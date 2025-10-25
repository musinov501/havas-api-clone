from typing import Dict

from .types import MessageTemplate

ACCOUNT_MESSAGES: Dict[str, MessageTemplate] = {
    "USER_CREATED": {
        "id": "USER_CREATED",
        "messages": {
            "en": "User account created successfully",
            "uz": "Foydalanuvchi hisobi muvaffaqiyatli yaratildi",
            "ru": "Учетная запись пользователя успешно создана",
        },
        "status_code": 201
    },
    "USER_NOT_FOUND": {
        "id": "USER_NOT_FOUND",
        "messages": {
            "en": "User with ID {user_id} not found",
            "uz": "ID {user_id} bo'lgan foydalanuvchi topilmadi",
            "ru": "Пользователь с ID {user_id} не найден",
        },
        "status_code": 404
    },
    "USER_ALREADY_EXISTS": {
        "id": "USER_ALREADY_EXISTS",
        "messages": {
            "en": "User with email {email} already exists",
            "uz": "{email} elektron pochtasi bilan foydalanuvchi allaqachon mavjud",
            "ru": "Пользователь с email {email} уже существует",
        },
        "status_code": 400
    },
    "INVALID_CREDENTIALS": {
        "id": "INVALID_CREDENTIALS",
        "messages": {
            "en": "Invalid email or password",
            "uz": "Noto'g'ri elektron pochta yoki parol",
            "ru": "Неверный email или пароль",
        },
        "status_code": 401
    },
    "ACCOUNT_DISABLED": {
        "id": "ACCOUNT_DISABLED",
        "messages": {
            "en": "Your account has been disabled",
            "uz": "Sizning hisobingiz o'chirilgan",
            "ru": "Ваша учетная запись была отключена",
        },
        "status_code": 403
    },
    "EMAIL_VERIFICATION_SENT": {
        "id": "EMAIL_VERIFICATION_SENT",
        "messages": {
            "en": "Verification email sent to {email}",
            "uz": "Tasdiqlash emaili {email} ga yuborildi",
            "ru": "Письмо с подтверждением отправлено на {email}",
        },
        "status_code": 200
    },
    "EMAIL_VERIFIED": {
        "id": "EMAIL_VERIFIED",
        "messages": {
            "en": "Email verified successfully",
            "uz": "Email muvaffaqiyatli tasdiqlandi",
            "ru": "Email успешно подтвержден",
        },
        "status_code": 200
    },
    "INVALID_TOKEN": {
        "id": "INVALID_TOKEN",
        "messages": {
            "en": "Invalid or expired token",
            "uz": "Noto'g'ri yoki muddati o'tgan token",
            "ru": "Недействительный или истекший токен",
        },
        "status_code": 400
    },
    "PASSWORD_CHANGED": {
        "id": "PASSWORD_CHANGED",
        "messages": {
            "en": "Password changed successfully",
            "uz": "Parol muvaffaqiyatli o'zgartirildi",
            "ru": "Пароль успешно изменен",
        },
        "status_code": 200
    },
    "PASSWORD_RESET_SENT": {
        "id": "PASSWORD_RESET_SENT",
        "messages": {
            "en": "Password reset instructions sent to your email",
            "uz": "Parolni tiklash bo'yicha ko'rsatmalar emailingizga yuborildi",
            "ru": "Инструкции по сбросу пароля отправлены на ваш email",
        },
        "status_code": 200
    },
}
