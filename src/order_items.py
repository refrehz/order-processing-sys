import logging

from fastapi import APIRouter
from pydantic import BaseModel

import sqlite3

log = logging.getLogger(__name__)
router = APIRouter()

DATABASE_FILE = "/app/db/local.db"


def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Create the authors table if it doesn't exist
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS OrderItems (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
        """
    )

    conn.commit()
    conn.close()


class OrderItems(BaseModel):
    order_id: int
    product_name: str
    quantity: int


@router.post('/v1/order-items')
async def create_order_item(order_items: OrderItems):

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Check if the order_id exists in the Orders table
    c.execute("SELECT order_id FROM Orders WHERE order_id=?", (order_items.order_id,))
    result = c.fetchone()

    if result is None:
        conn.close()
        return {"error": "Invalid order_id"}

    c.execute(
        'INSERT INTO OrderItems (order_id, product_name, quantity) VALUES (?, ?, ?)',
        (order_items.order_id, order_items.product_name, order_items.quantity)
    )

    order_items = c.lastrowid

    conn.commit()
    conn.close()

    log.debug(f'Created order item with ID: {order_items}')

    return {
        'item_id': order_items
    }


@router.get('/v1/order-items')
async def get_order_items():

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        """
        SELECT
            OrderItems.item_id,
            OrderItems.order_id,
            OrderItems.product_name,
            OrderItems.quantity
        FROM 
            OrderItems
        ORDER BY item_id DESC
        """
    )

    order_items = c.fetchall()

    conn.close()

    return {
        "order_items": [
            {
                "item_id": item[0],
                "order_id": item[1],
                "product_name": item[2],
                "quantity": item[3]
            }

            for item in order_items
        ]
    }