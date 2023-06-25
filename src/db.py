import sqlite3

# Create a connection to the database
conn = sqlite3.connect('/app/db/local.db')
cursor = conn.cursor()


async def initialize():

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            address TEXT
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderItems (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PaymentMethods (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            method TEXT,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
