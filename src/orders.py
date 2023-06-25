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
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )
        """
    )

    conn.commit()
    conn.close()


class Orders(BaseModel):
    customer_id: int
    order_date: str
    status: str


@router.post('/v1/orders')
async def create_order(orders: Orders):

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Check if the customer_id exists in the Customers table
    c.execute("SELECT customer_id FROM Customers WHERE customer_id=?", (orders.customer_id,))
    result = c.fetchone()

    if result is None:
        conn.close()
        return {"error": "Invalid customer_id"}

    c.execute(
        'INSERT INTO Orders (customer_id, order_date, status) VALUES (?, ?, ?)',
        (orders.customer_id, orders.order_date, orders.status)
    )

    conn.commit()
    order_id = c.lastrowid

    conn.close()

    log.debug(f'Created order with ID: {order_id}')

    return {'order_id': order_id}


@router.get('/v1/orders')
async def get_orders():

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        """
        SELECT
            Orders.order_id,
            Orders.customer_id,
            Orders.order_date,
            Orders.status
        FROM 
            Orders
        ORDER BY order_id DESC
        """
    )

    orders = c.fetchall()

    conn.close()

    return {
        "orders": [
            {
                "order_id": item[0],
                "customer_id": item[1],
                "order_date": item[2],
                "status": item[3]
            }

            for item in orders
        ]
    }