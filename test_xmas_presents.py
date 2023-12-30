import requests


BASE_URL = "http://127.0.0.1:8000"


# ------------------------------ GET Tests ------------------------------

def test_get_cadeaus():
    response = requests.get(f"{BASE_URL}/cadeaus")
    assert response.status_code == 200


# def test_get_present_by_id():
#     present_id = 1  # Dit moet een bestaand present_id zijn
#     response = requests.get(f"{BASE_URL}/cadeaus/{present_id}")
#     assert response.status_code == 200
#
#
# def test_get_present_names_by_category():
#     category = "speelgoed"  # Dit moet een bestaande categorie zijn
#     response = requests.get(f"{BASE_URL}/cadeaus/category/{category}")
#     assert response.status_code == 200


# ------------------------------ POST Tests ------------------------------

# def test_add_present():
#     present_data = {
#         "name": "Voorbeeld Cadeau",
#         "category": "Voorbeeld Categorie"
#     }
#
#     response = requests.post(f"{BASE_URL}/cadeau", json=present_data)
#     assert response.status_code == 201


# ------------------------------ PUT Tests ------------------------------

def test_update_present():
    present_id = 1
    updated_present_data = {
        "name": "Bijgewerkt Cadeau",
        "category": "Bijgewerkte Categorie"
    }

    response = requests.put(f"{BASE_URL}/cadeaus/{present_id}", json=updated_present_data)
    assert response.status_code == 200


# ------------------------------ DELETE Tests ------------------------------

# def test_delete_present():
#     present_id = 1
#
#     response = requests.delete(f"{BASE_URL}/cadeaus/{present_id}")
#     assert response.status_code == 200
