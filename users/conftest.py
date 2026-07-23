import pytest


@pytest.fixture
def test_user_data():
    return {
        "first_name": "Test",
        "last_name": "Testov",
        "phone": "+003",
        "email": "test@example.com",
        "password": "test.password",
        "re_password": "test.password",
    }


@pytest.fixture
def test_user_data2():
    return {
        "first_name": "Test",
        "last_name": "Testov",
        "phone": "+004",
        "email": "test2@example.com",
        "password": "test.password",
        "re_password": "test.password",
    }
