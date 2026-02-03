import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.mark.parametrize(
    "endpoint",
    ["/posts", "/comments", "/users", "/albums", "/photos", "/todos"],
)
def test_list_endpoints_return_200_and_non_empty(endpoint):
    response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_id_returns_expected_schema(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert "userId" in data
    assert "title" in data
    assert "body" in data


@pytest.mark.parametrize("post_id", [1, 5])
def test_comments_for_post_match_post_id(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(item["postId"] == post_id for item in data)


@pytest.mark.parametrize("post_id", [1, 3])
def test_nested_comments_match_query_filter(post_id):
    nested = requests.get(f"{BASE_URL}/posts/{post_id}/comments", timeout=10)
    filtered = requests.get(
        f"{BASE_URL}/comments",
        params={"postId": post_id},
        timeout=10,
    )
    assert nested.status_code == 200
    assert filtered.status_code == 200
    nested_data = nested.json()
    filtered_data = filtered.json()
    assert isinstance(nested_data, list)
    assert isinstance(filtered_data, list)
    assert len(nested_data) > 0
    assert len(filtered_data) > 0
    nested_ids = sorted(item["id"] for item in nested_data)
    filtered_ids = sorted(item["id"] for item in filtered_data)
    assert nested_ids == filtered_ids


def test_create_post_returns_201_and_echoes_payload():
    payload = {"title": "qa-home-test", "body": "sample", "userId": 10}
    response = requests.post(f"{BASE_URL}/posts", json=payload, timeout=10)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data


def test_update_post_put_returns_200_and_echoes_payload():
    payload = {"id": 1, "title": "put-title", "body": "put-body", "userId": 1}
    response = requests.put(f"{BASE_URL}/posts/1", json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == payload["id"]
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]


def test_patch_post_returns_200_and_merges_fields():
    payload = {"title": "patched-title"}
    response = requests.patch(f"{BASE_URL}/posts/1", json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert "body" in data
    assert "userId" in data


def test_delete_post_returns_200_and_empty_body():
    response = requests.delete(f"{BASE_URL}/posts/1", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data == {}
