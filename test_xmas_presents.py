import requests


BASE_URL = "http://127.0.0.1:8000"


def get_access_token(username: str, password: str):
    token_url = f"{BASE_URL}/token"
    token_data = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    response = requests.post(token_url, data=token_data)
    assert response.status_code == 200
    return response.json()["access_token"]


# ------------------------------ DELETE Tests ------------------------------

# Verwijder alle cadeaus
def test_delete_all_present():
    username = "test-username"
    password = "test-password"

    # Genereer een access token
    access_token = get_access_token(username, password)

    # Voer de DELETE-request uit met het gegenereerde token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(f"{BASE_URL}/cadeaus", headers=headers)

    # Controleer of de verwijdering is geslaagd
    assert response.status_code == 200


# Verwijder alle gebruikers
def test_delete_all_users():
    username = "test-username"
    password = "test-password"

    # Genereer een access token
    access_token = get_access_token(username, password)

    # Voer de DELETE-request uit met het gegenereerde token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200


# ------------------------------ POST Tests ------------------------------

# Maak een nieuw cadeau
def test_add_present():
    present_data = {
        "name": "Test Cadeau",
        "category": "Test Categorie"
    }

    response = requests.post(f"{BASE_URL}/cadeau", json=present_data)
    assert response.status_code == 200


# Maak een nieuwe gebruiker
def test_create_new_user():
    user_data = {
        "email": "test-username",
        "password": "test-password"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    assert response.status_code == 200


# ------------------------------ GET Tests ------------------------------

def test_get_cadeaus():
    response = requests.get(f"{BASE_URL}/cadeaus")
    assert response.status_code == 200


def test_get_present_by_id():
    present_id = 1  # Dit moet een bestaand present_id zijn
    response = requests.get(f"{BASE_URL}/cadeaus/{present_id}")
    assert response.status_code == 200


def test_get_present_names_by_category():
    category = "Test Categorie"  # Dit moet een bestaande categorie zijn
    response = requests.get(f"{BASE_URL}/cadeaus/category/{category}")
    assert response.status_code == 200


# ------------------------------ PUT Tests ------------------------------

def test_update_present():
    present_id = 1
    updated_present_data = {
        "name": "Bijgewerkt Test Cadeau",
        "category": "Bijgewerkte Test Categorie"
    }

    response = requests.put(f"{BASE_URL}/cadeaus/{present_id}", json=updated_present_data)
    assert response.status_code == 200


# ------------------------------ DELETE Tests ------------------------------
# Verwijder een cadeau
def test_delete_present():
    username = "test-username"
    password = "test-password"

    # Genereer een access token
    access_token = get_access_token(username, password)

    # Voer de DELETE-request uit met het gegenereerde token
    headers = {"Authorization": f"Bearer {access_token}"}

    present_id = 1

    response = requests.delete(f"{BASE_URL}/cadeaus/{present_id}", headers=headers)
    assert response.status_code == 200
