import pytest

from materials.models import Ad, Comment


@pytest.fixture
def ad_data(author_user):
    data = {"title": "Title 1", "description": "Some description", "price": 100.00, "author": author_user}
    return Ad.objects.create(**data)


@pytest.fixture
def comment_data(author_user, ad_data):
    data = {"text": "Some text", "ad": ad_data, "author": author_user}
    return Comment.objects.create(**data)
