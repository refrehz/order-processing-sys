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
        CREATE TABLE IF NOT EXISTS PaymentMethods (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            method TEXT,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
        """
    )

    conn.commit()
    conn.close()


class PaymentMethods(BaseModel):
    order_id: int
    method: str


@router.post('/v1/payment-methods')
async def create_payment_method(payment_methods: PaymentMethods):

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Check if the order_id exists in the Orders table
    c.execute("SELECT order_id FROM Orders WHERE order_id=?", (payment_methods.order_id,))
    result = c.fetchone()

    if result is None:
        conn.close()
        return {"error": "Invalid order_id"}

    c.execute(
        'INSERT INTO PaymentMethods (order_id, method) VALUES (?, ?)',
        (payment_methods.order_id, payment_methods.method)
    )

    payment_id = c.lastrowid

    conn.commit()
    conn.close()

    log.debug(f'Created payment method with ID: {payment_id}')

    return {
        'payment_id': payment_id
    }


@router.get('/v1/payment-methods')
async def get_payment_methods():

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        """
        SELECT
            PaymentMethods.payment_id,
            PaymentMethods.order_id,
            PaymentMethods.method
        FROM 
            PaymentMethods
        ORDER BY payment_id DESC
        """
    )

    payment_methods = c.fetchall()

    conn.close()

    return {
        "payment_methods": [
            {
                "payment_id": item[0],
                "order_id": item[1],
                "method": item[2]
            }

            for item in payment_methods
        ]
    }