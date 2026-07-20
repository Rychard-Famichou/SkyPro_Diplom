from drf_yasg.inspectors import SwaggerAutoSchema


class DjoserCustomSchema(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys=None):
        operation_id = super().get_operation_id(operation_keys)
        # Безопасно переименовываем ID операции для email авторизации
        if operation_id and "users_set_username" in operation_id:
            return operation_id.replace("username", "email")
        return operation_id

    def get_summary_and_description(self):
        try:
            result = super().get_summary_and_description()
            summary, description = result if result else (None, None)
        except Exception:
            summary, description = None, None

        path = getattr(self, "path", "")
        method = getattr(self, "method", "").lower()

        # Словарная карта путей Djoser и кастомных названий
        translations = {
            ("/users/", "get"): "Список пользователей",
            ("/users/", "post"): "Регистрация нового пользователя",
            ("/users/me/", "get"): "Получить мой профиль",
            ("/users/me/", "put"): "Обновить мой профиль (PUT)",
            ("/users/me/", "patch"): "Обновить мой профиль (PATCH)",
            ("/users/me/", "delete"): "Удалить мой профиль",
            ("/users/{id}/", "get"): "Получить профиль по id",
            ("/users/{id}/", "put"): "Обновить профиль по id (PUT)",
            ("/users/{id}/", "patch"): "Обновить профиль по id (PATCH)",
            ("/users/{id}/", "delete"): "Удалить профиль по id",
            ("/users/activation/", "post"): "Активация пользователя",
            ("/users/resend_activation/", "post"): "Выслать повторно письмо активации",
            ("/users/set_email/", "post"): "Смена текущего логина (Email)",
            ("/users/reset_email/", "post"): "Запрос на сброс логина (Email)",
            ("/users/reset_email_confirm/", "post"): "Подтверждение сброса логина (Email)",
            ("/users/set_password/", "post"): "Смена текущего пароля",
            ("/users/reset_password/", "post"): "Запрос на восстановление пароля",
            ("/users/reset_password_confirm/", "post"): "Подтверждение сброса пароля",
            # Эндпоинты JWT
            ("/jwt/create/", "post"): "Получение JWT-токена",
            ("/jwt/refresh/", "post"): "Обновление JWT-токена",
            ("/jwt/verify/", "post"): "Проверка валидности JWT-токена",
        }

        if (path, method) in translations:
            summary = translations[(path, method)]

        return summary, description
