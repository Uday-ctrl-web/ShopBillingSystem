import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "shop.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        total_amount REAL,
        date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL
    )
    """)

    conn.commit()
    conn.close()
def add_product(name, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
        (name, price, quantity)
    )

    conn.commit()
    conn.close()


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()
    return products
def update_product(product_id, name, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name = ?, price = ?, quantity = ?
        WHERE product_id = ?
        """,
        (name, price, quantity, product_id)
    )

    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE product_id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()
def add_customer(name, phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()
    customer_id = cursor.lastrowid
    conn.close()

    return customer_id


def create_sale(customer_id, total_amount, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sales (customer_id, total_amount, date) VALUES (?, ?, ?)",
        (customer_id, total_amount, date)
    )

    conn.commit()
    sale_id = cursor.lastrowid
    conn.close()

    return sale_id


def add_sale_item(sale_id, product_id, quantity, price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sale_items (sale_id, product_id, quantity, price)
        VALUES (?, ?, ?, ?)
        """,
        (sale_id, product_id, quantity, price)
    )

    cursor.execute(
        """
        UPDATE products
        SET quantity = quantity - ?
        WHERE product_id = ?
        """,
        (quantity, product_id)
    )

    conn.commit()
    conn.close()


def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT product_id, name, price, quantity FROM products WHERE product_id = ?",
        (product_id,)
    )

    product = cursor.fetchone()
    conn.close()

    return product
