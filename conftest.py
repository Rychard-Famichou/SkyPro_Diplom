from rest_framework.test import APIClient

import pytest

from users.models import CustomUser


@pytest.fixture
def guest_api_client() -> APIClient:
    """Фикстура для неавторизованного клиента DRF"""
    return APIClient()


@pytest.fixture
def test_user() -> CustomUser:
    """Фикстура для создания обычного пользователя"""
    return CustomUser.objects.create_user(
        first_name="Test", last_name="Testov", phone="+48600769182", email="test@example.com", password="test.password"
    )


@pytest.fixture
def test_user_auth_client(guest_api_client, test_user) -> APIClient:
    """Фикстура для авторизованного клиента DRF"""
    guest_api_client.force_authenticate(user=test_user)
    return guest_api_client
