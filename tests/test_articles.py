import json
import pytest

from rest_framework.reverse import reverse

from accounts.models import User
from articles.models import Article


@pytest.mark.django_db
def test_get_list_public_articles_as_anon(
    client,
    create_num_of_public_articles
):
    # given: anon user and num of public articles
    create_num_of_public_articles(10)
    # when: user is executing GET method
    url = reverse('articles')
    response = client.get(url)
    # then: expecting to get 200 and all articles
    assert response.status_code == 200
    assert len(response.data) == 10


@ pytest.mark.django_db
def test_get_detail_public_article_as_anon(
    client,
    create_public_article
):
    # given: anon user and public article
    article = create_public_article
    # when: anon user goes for detail of the public article
    url = reverse('articles_detail', args=[article.id])
    response = client.get(url)
    # then: expecting to get 200 and info on article
    assert response.status_code == 200
    assert response.data['id'] == article.id
    assert response.data['title'] == article.title
    assert response.data['description'] == article.description
    assert response.data['content'] == article.content
    assert response.data['author']['first_name'] == article.author.first_name
    assert response.data['author']['last_name'] == article.author.last_name


@pytest.mark.django_db
def test_get_list_private_articles_by_subscriber(
    create_user_with_role,
    basic_api_client_pass_user,
    create_num_of_private_articles
):
    # given: subcsriber client num of private articles
    subscriber = create_user_with_role(role=User.SUBSCRIBER)
    client = basic_api_client_pass_user(subscriber)
    create_num_of_private_articles(10)
    # when: client accesses the private articles
    url = reverse('articles')
    response = client.get(url)
    # then: expecting to get 200 and all info
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_private_article_by_subscriber(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article
):
    # given: subcsriber client and private article
    subscriber = create_user_with_role(role=User.SUBSCRIBER)
    client = basic_api_client_pass_user(subscriber)
    article = create_private_article
    # when: client accesses the private articles
    url = reverse('articles_detail', args=[article.id])
    response = client.get(url)
    # then: expecting to get 200 and all info
    assert response.status_code == 200
    assert response.data['id'] == article.id
    assert response.data['title'] == article.title
    assert response.data['description'] == article.description
    assert response.data['content'] == article.content
    assert response.data['author']['first_name'] == article.author.first_name
    assert response.data['author']['last_name'] == article.author.last_name
    assert response.data['visibility'] == article.visibility


@pytest.mark.django_db
def test_get_list_private_articles_by_anon(
    create_num_of_private_articles,
    client
):
    # given: anon client num of private articles
    create_num_of_private_articles(10)
    # when: client accesses the private articles
    url = reverse('articles')
    response = client.get(url)
    # then: expecting to get 200
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_get_private_article_by_anon(
    client,
    create_private_article
):
    # given: anon client and private article
    article = create_private_article
    # when: client accesses the private articles
    url = reverse('articles_detail', args=[article.id])
    response = client.get(url)
    # then: expecting to get 401 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to access this article.'


@pytest.mark.django_db
def test_post_public_article_as_author(
    basic_api_client_pass_user,
    create_user_with_role
):
    # given: author client
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    payload = {
        'title': 'test title',
        'description': 'test description',
        'content': 'test content',
    }
    # when: attemting to post article
    url = reverse('articles')
    response = client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expecting to get 201
    assert response.status_code == 201
    assert response.data['title'] == payload['title']
    assert response.data['description'] == payload['description']
    assert response.data['content'] == payload['content']
    assert response.data['visibility'] == Article.PUBLIC


@pytest.mark.django_db
def test_post_private_article_as_author(
    basic_api_client_pass_user,
    create_user_with_role
):
    # given: author client
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    payload = {
        'title': 'test title',
        'description': 'test description',
        'content': 'test content',
        'visibility': 'PRIVATE'
    }
    # when: attemting to post article
    url = reverse('articles')
    response = client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expecting to get 201
    assert response.status_code == 201
    assert response.data['title'] == payload['title']
    assert response.data['description'] == payload['description']
    assert response.data['content'] == payload['content']
    assert response.data['visibility'] == Article.PRIVATE


@pytest.mark.django_db
def test_post_public_article_as_subscriber(
    basic_api_client_pass_user,
    create_user_with_role
):
    # given: subscriber client
    subscriber = create_user_with_role(role=User.SUBSCRIBER)
    client = basic_api_client_pass_user(subscriber)
    payload = {
        'title': 'test title',
        'description': 'test description',
        'content': 'test content',
    }
    # when: attemting to post article
    url = reverse('articles')
    response = client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expecting to get 403
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_post_private_article_as_subscriber(
    basic_api_client_pass_user,
    create_user_with_role
):
    # given: author client
    subscriber = create_user_with_role(role=User.SUBSCRIBER)
    client = basic_api_client_pass_user(subscriber)
    payload = {
        'title': 'test title',
        'description': 'test description',
        'content': 'test content',
        'visibility': 'PRIVATE'
    }
    # when: attemting to post article
    url = reverse('articles')
    response = client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expecting to get 403
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_put_public_article_as_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_public_article_pass_author
):
    # given: article of author
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    article = create_public_article_pass_author(author)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
        'content': 'updated content',
        'visibility': 'PUBLIC'
    }
    # when: author is updateing the article
    url = reverse('articles_detail', args=[article.id])
    response = client.put(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 200 and updated values
    assert response.status_code == 200
    assert response.data['visibility'] == Article.PUBLIC
    assert response.data['title'] == payload['title']
    assert response.data['description'] == payload['description']
    assert response.data['content'] == payload['content']


@pytest.mark.django_db
def test_put_public_article_as_non_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_public_article_pass_author
):
    # given: article of author and another author
    author1 = create_user_with_role(role=User.AUTHOR)
    article = create_public_article_pass_author(author1)

    author2 = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author2)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
        'content': 'updated content',
        'visibility': 'PUBLIC'
    }
    # when: author2 is attempting to update the article of author1
    url = reverse('articles_detail', args=[article.id])
    response = client.put(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 403 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_patch_public_article_as_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_public_article_pass_author
):
    # given: article of author
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    article = create_public_article_pass_author(author)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
    }
    # when: author is updateing the article
    url = reverse('articles_detail', args=[article.id])
    response = client.patch(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 200 and updated values
    assert response.status_code == 200
    assert response.data['title'] == payload['title']
    assert response.data['description'] == payload['description']


@pytest.mark.django_db
def test_patch_public_article_as_non_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_public_article_pass_author
):
    # given: article of author and another author
    author1 = create_user_with_role(role=User.AUTHOR)
    article = create_public_article_pass_author(author1)

    author2 = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author2)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
    }
    # when: author is updateing the article
    url = reverse('articles_detail', args=[article.id])
    response = client.patch(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 403 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_delete_public_article_as_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_public_article_pass_author
):
    # given: article of author
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    article = create_public_article_pass_author(author)
    # when: author deletes article
    url = reverse('articles_detail', args=[article.id])
    response = client.delete(url)
    # then: expects to get 204 code
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_public_article_as_non_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_public_article_pass_author
):
    # given: article of author
    author1 = create_user_with_role(role=User.AUTHOR)
    article = create_public_article_pass_author(author1)

    author2 = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author2)
    # when: author deletes article
    url = reverse('articles_detail', args=[article.id])
    response = client.delete(url)
    # then: expect to get 403 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_put_private_article_as_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article_pass_author
):
    # given: article of author
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    article = create_private_article_pass_author(author)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
        'content': 'updated content',
        'visibility': 'PRIVATE'
    }
    # when: author is updateing the article
    url = reverse('articles_detail', args=[article.id])
    response = client.put(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 200 and updated values
    assert response.status_code == 200
    assert response.data['visibility'] == Article.PRIVATE
    assert response.data['title'] == payload['title']
    assert response.data['description'] == payload['description']
    assert response.data['content'] == payload['content']


@pytest.mark.django_db
def test_put_private_article_as_non_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article_pass_author
):
    # given: article of author and another author
    author1 = create_user_with_role(role=User.AUTHOR)
    article = create_private_article_pass_author(author1)

    author2 = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author2)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
        'content': 'updated content',
        'visibility': 'PRIVATE'
    }
    # when: author2 is attempting to update the article of author1
    url = reverse('articles_detail', args=[article.id])
    response = client.put(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 403 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_patch_private_article_as_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article_pass_author
):
    # given: article of author
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    article = create_private_article_pass_author(author)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
    }
    # when: author is updateing the article
    url = reverse('articles_detail', args=[article.id])
    response = client.patch(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 200 and updated values
    assert response.status_code == 200
    assert response.data['title'] == payload['title']
    assert response.data['description'] == payload['description']


@pytest.mark.django_db
def test_patch_private_article_as_non_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article_pass_author
):
    # given: article of author and another author
    author1 = create_user_with_role(role=User.AUTHOR)
    article = create_private_article_pass_author(author1)

    author2 = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author2)
    payload = {
        'title': 'updated title',
        'description': 'updated description',
    }
    # when: author is updateing the article
    url = reverse('articles_detail', args=[article.id])
    response = client.patch(
        url,
        data=json.dumps(payload),
        content_type='application/json'
    )
    # then: expect to get 403 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'


@pytest.mark.django_db
def test_delete_private_article_as_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article_pass_author
):
    # given: article of author
    author = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author)
    article = create_private_article_pass_author(author)
    # when: author deletes article
    url = reverse('articles_detail', args=[article.id])
    response = client.delete(url)
    # then: expects to get 204 code
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_private_article_as_non_author(
    create_user_with_role,
    basic_api_client_pass_user,
    create_private_article_pass_author
):
    # given: article of author
    author1 = create_user_with_role(role=User.AUTHOR)
    article = create_private_article_pass_author(author1)

    author2 = create_user_with_role(role=User.AUTHOR)
    client = basic_api_client_pass_user(author2)
    # when: author deletes article
    url = reverse('articles_detail', args=[article.id])
    response = client.delete(url)
    # then: expect to get 403 and detail
    assert response.status_code == 403
    assert response.data['detail'] == 'You are not allowed to perform this action.'
