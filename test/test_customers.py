import requests


def test_customers():

    url = 'http://localhost:8000/v1/customer/'

    data = {
        "name": "Test Customer",
        "email": "test@test.com",
        "address": "123 Test St"
    }

    response = requests.post(url, json=data)
    response1 = requests.get(url)

    assert response.json() == {"customer_id": 1}
    assert response1.json() == {"customers": [{"customer_id": 1, "name": "Test Customer",
                                               "email": "test@test.com", "address": "123 Test St", }]}
