"""SQLite operations for the Lab 5 user management API."""

import os
import sqlite3
from contextlib import closing
from pathlib import Path


DEFAULT_DATABASE = Path(__file__).resolve().parent / "database.db"
USER_FIELDS = ("name", "email", "phone", "address", "country")
INITIAL_USERS = (
    {
        "user_id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "067765434567",
        "address": "John Doe Street, Innsbruck",
        "country": "Austria",
    },
)


def database_path():
    """Allow tests and deployments to select a database without changing code."""
    return Path(os.environ.get("FLASK_USER_DB", DEFAULT_DATABASE))


def connect_to_db():
    connection = sqlite3.connect(database_path())
    connection.row_factory = sqlite3.Row
    return connection


def create_db_table():
    with closing(connect_to_db()) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            )
            """
        )
        connection.executemany(
            "INSERT OR IGNORE INTO users "
            "(user_id, name, email, phone, address, country) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                (
                    user["user_id"],
                    user["name"],
                    user["email"],
                    user["phone"],
                    user["address"],
                    user["country"],
                )
                for user in INITIAL_USERS
            ],
        )


def get_users():
    with closing(connect_to_db()) as connection:
        rows = connection.execute("SELECT * FROM users ORDER BY user_id").fetchall()
        return [dict(row) for row in rows]


def get_user_by_id(user_id):
    with closing(connect_to_db()) as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row is not None else None


def insert_user(user):
    values = tuple(user[field] for field in USER_FIELDS)
    with closing(connect_to_db()) as connection, connection:
        cursor = connection.execute(
            "INSERT INTO users (name, email, phone, address, country) "
            "VALUES (?, ?, ?, ?, ?)",
            values,
        )
        user_id = cursor.lastrowid
    return get_user_by_id(user_id)


def update_user(user):
    values = tuple(user[field] for field in USER_FIELDS) + (user["user_id"],)
    with closing(connect_to_db()) as connection, connection:
        cursor = connection.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, "
            "country = ? WHERE user_id = ?",
            values,
        )
        changed = cursor.rowcount
    return get_user_by_id(user["user_id"]) if changed else None


def delete_user(user_id):
    with closing(connect_to_db()) as connection, connection:
        cursor = connection.execute(
            "DELETE FROM users WHERE user_id = ?", (user_id,)
        )
        return cursor.rowcount > 0


if __name__ == "__main__":
    create_db_table()
    print(f"Database ready: {database_path()}")
