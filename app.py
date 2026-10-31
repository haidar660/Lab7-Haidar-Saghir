"""Flask REST API for managing users in SQLite."""

from flask import Flask, jsonify, request
from flask_cors import CORS

from database import (
    USER_FIELDS,
    create_db_table,
    delete_user,
    get_user_by_id,
    get_users,
    insert_user,
    update_user,
)


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
create_db_table()


def valid_user_payload(payload, *, updating=False):
    if not isinstance(payload, dict):
        return False
    if any(
        not isinstance(payload.get(field), str) or not payload[field].strip()
        for field in USER_FIELDS
    ):
        return False
    if updating and (
        type(payload.get("user_id")) is not int or payload["user_id"] < 1
    ):
        return False
    return True


@app.get("/api/users")
def api_get_users():
    return jsonify(get_users())


@app.get("/api/users/<int:user_id>")
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify(error="User not found"), 404
    return jsonify(user)


@app.post("/api/users/add")
def api_add_user():
    user = request.get_json(silent=True)
    if not valid_user_payload(user):
        return jsonify(error="Provide name, email, phone, address, and country"), 400
    return jsonify(insert_user(user)), 201


@app.put("/api/users/update")
def api_update_user():
    user = request.get_json(silent=True)
    if not valid_user_payload(user, updating=True):
        return jsonify(
            error="Provide a positive integer user_id and all five user fields"
        ), 400
    updated = update_user(user)
    if updated is None:
        return jsonify(error="User not found"), 404
    return jsonify(updated)


@app.delete("/api/users/delete/<int:user_id>")
def api_delete_user(user_id):
    if not delete_user(user_id):
        return jsonify(error="User not found"), 404
    return jsonify(status="User deleted successfully")


if __name__ == "__main__":
    app.run()
