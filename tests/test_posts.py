from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    # print(res.json())
    post_list = res.json()
    validated_data = [schemas.PostOut(**item) for item in post_list]

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/99999")

    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content
    assert post.post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscraper", "wahoo", True), ])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "title1", "content": "content1"})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "title1"
    assert created_post.content == "content1"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "title1", "content": "content1"})

    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/99999")

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    post = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post)
    updated_post = schemas.Post(**res.json())

    assert updated_post.title == post['title']
    assert updated_post.content == post['content']
    assert updated_post.id == post['id']
    assert updated_post.owner_id == test_user['id']

    assert res.status_code == 200

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    post = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post)

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    post = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }

    res = client.put(f"/posts/{test_posts[0].id}", json=post)

    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):

    post = {
        "title": "Updated title",
        "content": "Updated content",
        "id": test_posts[0].id
    }
    
    res = authorized_client.put(f"/posts/99999", json=post)

    assert res.status_code == 404