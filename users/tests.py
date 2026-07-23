import re

from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from rest_framework import status

import pytest


# Create your tests here.
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


@pytest.mark.django_db
class TestCreateUserAPI:
    create_url = reverse_lazy("customuser-list")

    def test_create_user_success(self, guest_api_client, test_user_data):
        response = guest_api_client.post(self.create_url, data=test_user_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == test_user_data["email"]
        assert response.data["first_name"] == test_user_data["first_name"]
        assert "password" not in response.data

    @pytest.mark.parametrize(
        "invalid_field, invalid_value, expected_exception",
        [
            ("email", "", ValueError),
            ("first_name", "", ValueError),
            ("last_name", "", ValueError),
            ("phone", "", ValidationError),
            ("password", "", ValidationError),
            ("re_password", "", ValidationError),
        ],
    )
    def test_create_user_missing_required_fields(
        self, guest_api_client, test_user_data, invalid_field, invalid_value, expected_exception
    ):
        test_user_data[invalid_field] = invalid_value
        response = guest_api_client.post(self.create_url, data=test_user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invalid_field in response.data

    def test_create_user_mismatched_passwords(self, guest_api_client, test_user_data):
        test_user_data["re_password"] = "different_password"
        response = guest_api_client.post(self.create_url, data=test_user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data or "re_password" in response.data


@pytest.mark.django_db
class TestRUDUserAPI:
    me_url = reverse_lazy("customuser-me")

    def test_detail(self, user_auth_client):
        response = user_auth_client.get(self.me_url)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, user_auth_client):
        patch_data = {
            "first_name": "Test2",
        }
        response = user_auth_client.patch(self.me_url, data=patch_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Test2"

    def test_put(self, user_auth_client):
        put_data = {"first_name": "Test3", "last_name": "Test4", "phone": "+007"}
        response = user_auth_client.put(self.me_url, data=put_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Test3"
        assert response.data["last_name"] == "Test4"
        assert response.data["phone"] == "+007"

    def test_delete(self, user_auth_client):
        delete_data = {"current_password": "test.password"}
        response = user_auth_client.delete(self.me_url, data=delete_data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None


@pytest.mark.django_db
class TestResetPasswordAPI:
    reset_url = reverse_lazy("customuser-reset-password")
    reset_confirm_url = reverse_lazy("customuser-reset-password-confirm")

    def test_reset_password(self, guest_api_client, simple_user, mailoutbox):
        email_data = {"email": simple_user.email}
        response = guest_api_client.post(self.reset_url, data=email_data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert len(mailoutbox) == 1
        email = mailoutbox[0]
        assert simple_user.email in email.to
        match = re.search(r"confirm/([^/]+)/([^/\s\n]+)", email.body)
        assert match is not None, "Не удалось найти uid и token в тексте письма"
        uid = match.group(1)
        token = match.group(2)
        confirm_payload = {"uid": uid, "token": token, "new_password": "new.test.password"}

        confirm_response = guest_api_client.post(self.reset_confirm_url, data=confirm_payload)
        assert confirm_response.status_code == status.HTTP_204_NO_CONTENT
        simple_user.refresh_from_db()
        assert simple_user.check_password("new.test.password") is True
