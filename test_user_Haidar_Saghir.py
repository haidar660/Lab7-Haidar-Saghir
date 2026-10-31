"""Lab 7 Pytest tests for the Flask user application."""

from contextlib import closing

import pytest

from database import (
    INITIAL_USERS,
    connect_to_db,
    create_db_table,
    delete_user,
    get_user_by_id,
    get_users,
    insert_user,
    update_user,
)


@pytest.fixture
def database_file(tmp_path, monkeypatch):
    """Create the same database that the application creates on its first run."""
    path = tmp_path / "test_database.db"
    monkeypatch.setenv("FLASK_USER_DB", str(path))
    create_db_table()
    return path


@pytest.fixture
def empty_database(database_file):
    """Provide an isolated database without the initial user for CRUD tests."""
    with closing(connect_to_db()) as connection, connection:
        connection.execute("DELETE FROM users")
    return database_file


@pytest.fixture
def client(empty_database):
    """Provide Flask's test client connected to the isolated database."""
    from app import app

    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def sample_user():
    return {
        "name": "Haidar Saghir",
        "email": "haidar.saghir@example.com",
        "phone": "70123456",
        "address": "Beirut",
        "country": "Lebanon",
    }


@pytest.fixture
def second_user():
    return {
        "name": "Sarah Khalil",
        "email": "sarah.khalil@example.com",
        "phone": "76123456",
        "address": "Tripoli",
        "country": "Lebanon",
    }


def test_database_is_created_with_specified_users(database_file):
    assert database_file.exists()
    assert get_users() == [dict(user) for user in INITIAL_USERS]


def test_insert_user(empty_database, sample_user):
    inserted = insert_user(sample_user)

    assert inserted == {"user_id": 1, **sample_user}
    assert get_user_by_id(inserted["user_id"]) == inserted


def test_get_users(empty_database, sample_user, second_user):
    first = insert_user(sample_user)
    second = insert_user(second_user)

    assert get_users() == [first, second]


def test_get_users_by_id(empty_database, sample_user):
    inserted = insert_user(sample_user)

    assert get_user_by_id(inserted["user_id"]) == inserted
    assert get_user_by_id(999) is None


def test_update_user(empty_database, sample_user):
    inserted = insert_user(sample_user)
    updated_data = {**inserted, "phone": "70999999", "address": "Saida"}

    updated = update_user(updated_data)

    assert updated == updated_data
    assert get_user_by_id(inserted["user_id"]) == updated_data


def test_delete_user(empty_database, sample_user):
    inserted = insert_user(sample_user)

    assert delete_user(inserted["user_id"]) is True
    assert get_user_by_id(inserted["user_id"]) is None
    assert delete_user(inserted["user_id"]) is False


def test_api_get_user(client, sample_user):
    inserted = insert_user(sample_user)

    response = client.get(f"/api/users/{inserted['user_id']}")

    assert response.status_code == 200
    assert response.get_json() == inserted


def test_api_add_user(client, sample_user):
    response = client.post("/api/users/add", json=sample_user)

    assert response.status_code == 201
    assert response.get_json() == {"user_id": 1, **sample_user}
    assert get_user_by_id(1) == response.get_json()


def test_api_update_user(client, sample_user):
    inserted = insert_user(sample_user)
    uploaded_data = {**inserted, "country": "Canada"}

    response = client.put("/api/users/update", json=uploaded_data)

    assert response.status_code == 200
    assert response.get_json() == uploaded_data
    assert get_user_by_id(inserted["user_id"]) == uploaded_data


def test_api_delete_user(client, sample_user):
    inserted = insert_user(sample_user)

    response = client.delete(f"/api/users/delete/{inserted['user_id']}")

    assert response.status_code == 200
    assert response.get_json() == {"status": "User deleted successfully"}
    assert get_user_by_id(inserted["user_id"]) is None
