"""
setup_database.py
------------------
Creates a small sample e-commerce SQLite database (sample_data.db) with
customers, products, and orders, so you have real data to query.

Run this once before using cli.py or app.py:
    python setup_database.py
"""

import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "sample_data.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Drop tables if they already exist, so this script can be re-run safely
    cur.executescript("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
    """)

    cur.executescript("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            city TEXT NOT NULL,
            signup_date TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit_price REAL NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)

    cities = ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune"]
    customers = [
        (i, f"Customer {i}", random.choice(cities),
         (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d"))
        for i in range(1, 31)
    ]
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?)", customers)

    products = [
        (1, "Wireless Mouse", "Electronics", 599.0),
        (2, "Mechanical Keyboard", "Electronics", 2499.0),
        (3, "USB-C Cable", "Electronics", 299.0),
        (4, "Notebook", "Stationery", 99.0),
        (5, "Desk Lamp", "Home & Office", 899.0),
        (6, "Office Chair", "Home & Office", 5999.0),
        (7, "Water Bottle", "Lifestyle", 349.0),
        (8, "Backpack", "Lifestyle", 1599.0),
        (9, "Monitor Stand", "Electronics", 1299.0),
        (10, "Sticky Notes Pack", "Stationery", 149.0),
    ]
    cur.executemany("INSERT INTO products VALUES (?,?,?,?)", products)

    orders = []
    order_items = []
    order_item_id = 1
    for order_id in range(1, 121):
        customer_id = random.randint(1, 30)
        order_date = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 550))).strftime("%Y-%m-%d")
        orders.append((order_id, customer_id, order_date))

        num_items = random.randint(1, 4)
        chosen_products = random.sample(range(1, 11), num_items)
        for product_id in chosen_products:
            quantity = random.randint(1, 5)
            order_items.append((order_item_id, order_id, product_id, quantity))
            order_item_id += 1

    cur.executemany("INSERT INTO orders VALUES (?,?,?)", orders)
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?)", order_items)

    conn.commit()
    conn.close()
    print(f"Created {DB_NAME} with sample customers, products, orders, and order_items.")


if __name__ == "__main__":
    create_database()
