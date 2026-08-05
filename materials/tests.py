from django.urls import reverse_lazy

import pytest

from materials.models import Ad, Comment


# Create your tests here.
@pytest.mark.django_db
class TestAdListApi:
    """Класс для тестирования списка Объявлений"""
    ad_list_url = reverse_lazy("materials:ad-list")

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 0),
            ("user_auth_client", 0),
            ("author_auth_client", 0),
            ("admin_auth_client", 0),
        ],
    )
    def test_list(self, request, client_fixture_name, expected):
        """Тест: список объявлений доступен всем"""

        client = request.getfixturevalue(client_fixture_name)
        response = client.get(self.ad_list_url)
        assert response.status_code == 200
        assert response.data["count"] == expected

    def test_filter(self, user_auth_client, ad_data):
        """Тест: фильтр списка"""
        response = user_auth_client.get(self.ad_list_url, data={"title": "1"})
        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["title"] == "Title 1"

    def test_filter_empty(self, user_auth_client):
        """Тест: фильтр списка"""
        response = user_auth_client.get(self.ad_list_url, data={"title": "1"})
        assert response.status_code == 200
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0


@pytest.mark.django_db
class TestAdCRUDApi:
    """Класс для тестирования полного цикла для Объявления"""

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 201),
            ("author_auth_client", 201),
            ("admin_auth_client", 201),
        ],
    )
    def test_create(self, request, client_fixture_name, expected):
        ads_create_url = reverse_lazy("materials:ad-create")
        data = {
            "title": "test title",
            "description": "test description",
            "price": 100.00,
            "author": client_fixture_name,
        }
        client = request.getfixturevalue(client_fixture_name)
        response = client.post(ads_create_url, data=data, format="json")
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 200),
            ("author_auth_client", 200),
            ("admin_auth_client", 200),
        ],
    )
    def test_detail(self, request, client_fixture_name, expected, ad_data):
        ads_detail_url = reverse_lazy("materials:ad-detail", kwargs={"pk": ad_data.pk})
        client = request.getfixturevalue(client_fixture_name)
        response = client.get(ads_detail_url)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "client_fixture_name, expected, new_data",
        [
            ("guest_api_client", 401, {"description": "New guest description"}),
            ("user_auth_client", 403, {"description": "New user description"}),
            ("author_auth_client", 200, {"description": "New author description"}),
            ("admin_auth_client", 200, {"description": "New admin description"}),
        ],
    )
    def test_update(self, request, client_fixture_name, expected, new_data, ad_data):
        ads_update_url = reverse_lazy("materials:ad-update", kwargs={"pk": ad_data.pk})
        client = request.getfixturevalue(client_fixture_name)
        response = client.patch(ads_update_url, data=new_data, format="json")
        assert response.status_code == expected
        if expected == 200:
            assert response.data["description"] == new_data["description"]
            ad_data.refresh_from_db()
            assert ad_data.description == new_data["description"]
        else:
            ad_data.refresh_from_db()
            assert ad_data.description == "Some description"

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 403),
            ("author_auth_client", 204),
            ("admin_auth_client", 204),
        ],
    )
    def test_delete(self, request, client_fixture_name, expected, ad_data):
        ads_delete_url = reverse_lazy("materials:ad-delete", kwargs={"pk": ad_data.pk})
        client = request.getfixturevalue(client_fixture_name)
        response = client.delete(ads_delete_url)
        assert response.status_code == expected
        if expected == 204:
            assert not Ad.objects.filter(pk=ad_data.pk).exists()
        else:
            assert Ad.objects.filter(pk=ad_data.pk).exists()


@pytest.mark.django_db
class TestCommentListApi:
    """Класс для тестирования списка Комментариев"""

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 200),
            ("author_auth_client", 200),
            ("admin_auth_client", 200),
        ],
    )
    def test_list(self, request, client_fixture_name, expected):
        comment_list_url = reverse_lazy("materials:comment-list")
        client = request.getfixturevalue(client_fixture_name)
        response = client.get(comment_list_url)
        assert response.status_code == expected


@pytest.mark.django_db
class TestCommentCRUDApi:
    """Класс для тестирования полного цикла для Комментариев"""

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 201),
            ("author_auth_client", 201),
            ("admin_auth_client", 201),
        ],
    )
    def test_create(self, request, client_fixture_name, expected, ad_data):
        comment_create_url = reverse_lazy("materials:comment-create")
        data = {"text": "test text", "ad": ad_data.pk, "author": client_fixture_name}
        client = request.getfixturevalue(client_fixture_name)
        response = client.post(comment_create_url, data=data, format="json")
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 200),
            ("author_auth_client", 200),
            ("admin_auth_client", 200),
        ],
    )
    def test_detail(self, request, client_fixture_name, expected, comment_data):
        comment_detail_url = reverse_lazy("materials:comment-detail", kwargs={"pk": comment_data.pk})
        client = request.getfixturevalue(client_fixture_name)
        response = client.get(comment_detail_url)
        assert response.status_code == expected

    @pytest.mark.parametrize(
        "client_fixture_name, expected, new_data",
        [
            ("guest_api_client", 401, {"text": "New guest text"}),
            ("user_auth_client", 403, {"text": "New user text"}),
            ("author_auth_client", 200, {"text": "New author text"}),
            ("admin_auth_client", 200, {"text": "New admin text"}),
        ],
    )
    def test_update(self, request, client_fixture_name, expected, new_data, comment_data):
        comment_update_url = reverse_lazy("materials:comment-update", kwargs={"pk": comment_data.pk})
        client = request.getfixturevalue(client_fixture_name)
        response = client.patch(comment_update_url, data=new_data, format="json")
        assert response.status_code == expected
        if expected == 200:
            assert response.data["text"] == new_data["text"]
            comment_data.refresh_from_db()
            assert comment_data.text == new_data["text"]
        else:
            comment_data.refresh_from_db()
            assert comment_data.text == "Some text"

    @pytest.mark.parametrize(
        "client_fixture_name, expected",
        [
            ("guest_api_client", 401),
            ("user_auth_client", 403),
            ("author_auth_client", 204),
            ("admin_auth_client", 204),
        ],
    )
    def test_delete(self, request, client_fixture_name, expected, comment_data):
        comment_delete_url = reverse_lazy("materials:comment-delete", kwargs={"pk": comment_data.pk})
        client = request.getfixturevalue(client_fixture_name)
        response = client.delete(comment_delete_url)
        assert response.status_code == expected
        if expected == 204:
            assert not Comment.objects.filter(pk=comment_data.pk).exists()
        else:
            assert Comment.objects.filter(pk=comment_data.pk).exists()
