from rest_framework.test import APIClient

import pytest

from users.models import CustomUser


@pytest.fixture
def guest_api_client() -> APIClient:
    """Фикстура для неавторизованного клиента DRF"""
    return APIClient()


@pytest.fixture
def simple_user() -> CustomUser:
    """Фикстура для создания обычного пользователя"""
    return CustomUser.objects.create_user(
        first_name="Test", last_name="Testov", phone="+003", email="test@example.com", password="test.password"
    )


@pytest.fixture
def author_user() -> CustomUser:
    """Фикстура для создания автора контента"""
    return CustomUser.objects.create_user(
        first_name="Author", last_name="Authorov", phone="+002", email="author@example.com", password="author.password"
    )


@pytest.fixture
def admin_user() -> CustomUser:
    """Фикстура для создания администратора"""
    return CustomUser.objects.create_user(
        first_name="Admin",
        last_name="Adminov",
        phone="+001",
        email="admin@example.com",
        password="admin.password",
        role="ADMIN",
    )


@pytest.fixture
def user_auth_client(simple_user) -> APIClient:
    """Фикстура для авторизованного пользователя"""
    client = APIClient()
    client.force_authenticate(user=simple_user)
    return client


@pytest.fixture
def author_auth_client(author_user) -> APIClient:
    """Фикстура для авторизованного автора контента"""
    client = APIClient()
    client.force_authenticate(user=author_user)
    return client


@pytest.fixture
def admin_auth_client(admin_user) -> APIClient:
    """Фикстура для авторизованного администратора"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
