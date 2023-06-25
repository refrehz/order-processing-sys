import requests


def test_order_items():
    url = 'http://localhost:8000/v1/order-items/'

    # Valid order item data
    valid_data = {
        "order_id": 1,
        "product_name": "snickers",
        "quantity": 1
    }

    # Invalid order item data with non-existent order_id
    invalid_data = {
        "order_id": 9999,
        "product_name": "invalid product",
        "quantity": 2
    }

    # Test valid order item creation
    response = requests.post(url, json=valid_data)
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

    # Test retrieving order items
    response1 = requests.get(url)
    assert response1.status_code == 200
    assert response1.json() == {
        "order_items": [
            {
                "item_id": 1,
                "order_id": 1,
                "product_name": "snickers",
                "quantity": 1
            }
        ]
    }

    # Test invalid order item creation
    response_invalid = requests.post(url, json=invalid_data)
    assert response_invalid.status_code == 200
    assert response_invalid.json() == {"error": "Invalid order_id"}
