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
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


class Customers(BaseModel):
    name: str
    email: str
    address: str


@router.post('/v1/customer/')
async def add_customer(customer: Customers):

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        'INSERT INTO Customers (name, email, address) VALUES (?, ?, ?)',
        (customer.name, customer.email, customer.address))

    # Get the last inserted row id (customer_id)
    customer_id = c.lastrowid

    conn.commit()
    conn.close()

    log.debug(f'Created customer with ID: {customer_id}')
    return {"customer_id": customer_id}


@router.get('/v1/customer/')
async def get_customers():

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute(
        """
        SELECT
            Customers.customer_id,
            Customers.name,
            Customers.email,
            Customers.address
        FROM 
            Customers
        ORDER BY customer_id DESC

    """)

    customers = c.fetchall()

    conn.close()

    return {
        "customers": [
            {
                "customer_id": item[0],
                "name": item[1],
                "email": item[2],
                "address": item[3]
            }
            for item in customers
        ]
    }

create_database()
