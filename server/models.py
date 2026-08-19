import sqlite3


DATABASE = "inventory.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_all_items():
    connection = get_connection()

    items = connection.execute(
        "SELECT * FROM inventory"
    ).fetchall()

    connection.close()

    return [dict(item) for item in items]


def get_item(item_id):
    connection = get_connection()

    item = connection.execute(
        "SELECT * FROM inventory WHERE id = ?",
        (item_id,)
    ).fetchone()

    connection.close()

    if item is None:
        return None

    return dict(item)


def add_item(name, barcode, quantity, price):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO inventory (name, barcode, quantity, price)
        VALUES (?, ?, ?, ?)
        """,
        (name, barcode, quantity, price)
    )

    connection.commit()

    item_id = cursor.lastrowid

    connection.close()

    return get_item(item_id)


def update_item(item_id, name, barcode, quantity, price):
    connection = get_connection()

    connection.execute(
        """
        UPDATE inventory
        SET name = ?, barcode = ?, quantity = ?, price = ?
        WHERE id = ?
        """,
        (name, barcode, quantity, price, item_id)
    )

    connection.commit()
    connection.close()

    return get_item(item_id)


def delete_item(item_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM inventory WHERE id = ?",
        (item_id,)
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted