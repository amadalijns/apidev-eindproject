import requests


BASE_URL = "http://127.0.0.1:8000"


def test_get_cadeaus():
    response = requests.get(f"{BASE_URL}/cadeaus")
    assert response.status_code == 200


def test_get_present_by_id():
    present_id = 1  # Vervang dit door een geldig present_id
    response = requests.get(f"{BASE_URL}/cadeaus/{present_id}")
    assert response.status_code == 200
