import base64
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from accounts.models import User
from articles.models import Article
from tests.factories import ArticleFactory, UserFactory

register(UserFactory)
register(ArticleFactory)


@pytest.fixture
def create_user_with_role(db) -> UserFactory:
    def make_user_with_role(role: str = User.SUBSCRIBER, **kwargs):
        if role == User.ADMIN:
            return UserFactory.create(admin=True, **kwargs)
        if role == User.AUTHOR:
            return UserFactory.create(author=True, **kwargs)
        return UserFactory.create(**kwargs)
    return make_user_with_role


@pytest.fixture
def basic_api_client_pass_user(db):
    def make_client_pass_user(user: User):
        client = APIClient()
        creds = base64.b64encode(f'{user.email}:veryStrongP@$$123'.encode()).decode()
        client.credentials(HTTP_AUTHORIZATION=f'Basic {creds}')
        return client
    return make_client_pass_user


@pytest.fixture
def create_num_of_public_articles(db) -> ArticleFactory:
    def make_num_of_articles(num: int = 1) -> list[Article]:
        return ArticleFactory.create_batch(size=num)
    return make_num_of_articles


@pytest.fixture
def create_public_article(db):
    return ArticleFactory()


@pytest.fixture
def create_public_article_pass_author(db):
    def make_article_with_author_user(user: User) -> Article:
        return ArticleFactory.create(author=user)
    return make_article_with_author_user        


@pytest.fixture
def create_num_of_private_articles(db) -> ArticleFactory:
    def make_num_of_articles(num: int = 1) -> list[Article]:
        return ArticleFactory.create_batch(size=num, private=True)
    return make_num_of_articles


@pytest.fixture
def create_private_article(db):
    return ArticleFactory.create(private=True)


@pytest.fixture
def create_private_article_pass_author(db):
    def make_article_with_author_user(user: User) -> Article:
        return ArticleFactory.create(author=user, private=True)
    return make_article_with_author_user


@pytest.fixture
def anon_api_client():
    return APIClient()



