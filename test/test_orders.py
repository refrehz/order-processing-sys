import requests


def test_orders():
    url = 'http://localhost:8000/v1/orders/'

    data = {
        "customer_id": 1,
        "order_date": "11.10.2023",
        "status": "payment successful"
    }

    response = requests.post(url, json=data)
    response1 = requests.get(url)

    assert response.json() == {"order_id": 1}
    assert response1.json() == {"orders": [{"order_id": 1, "customer_id": 1,
                                            "order_date": "11.10.2023", "status": "payment successful"}]}
