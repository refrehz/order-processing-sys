import requests


def test_payment_methods():
    url = 'http://localhost:8000/v1/payment-methods/'

    data = {
        "payment_id": 1,
        "order_id": 1,
        "method": "credit card"
    }

    response = requests.post(url, json=data)
    response1 = requests.get(url)

    assert response.json() == {"payment_id": 1}
    assert response1.json() == {"payment_methods": [{"payment_id": 1,
                                                     "order_id": 1,
                                                     "method": "credit card"}]}