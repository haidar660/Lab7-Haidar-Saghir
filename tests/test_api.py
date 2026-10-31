"""Exercise the CRUD flow and important error responses."""

import os
import tempfile
import unittest


class UserApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.previous_db = os.environ.get("FLASK_USER_DB")
        os.environ["FLASK_USER_DB"] = os.path.join(cls.temp_dir.name, "test.db")
        from app import app
        from database import create_db_table

        cls.app = app
        create_db_table()

    @classmethod
    def tearDownClass(cls):
        if cls.previous_db is None:
            os.environ.pop("FLASK_USER_DB", None)
        else:
            os.environ["FLASK_USER_DB"] = cls.previous_db
        cls.temp_dir.cleanup()

    def setUp(self):
        self.client = self.app.test_client()

    def test_full_crud_flow(self):
        user = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "067765434567",
            "address": "John Doe Street, Innsbruck",
            "country": "Austria",
        }
        response = self.client.post("/api/users/add", json=user)
        self.assertEqual(response.status_code, 201)
        created = response.get_json()
        user_id = created["user_id"]
        self.assertEqual(created["name"], user["name"])

        response = self.client.get("/api/users")
        self.assertEqual(response.status_code, 200)
        self.assertIn(created, response.get_json())

        response = self.client.get(f"/api/users/{user_id}")
        self.assertEqual(response.get_json(), created)

        response = self.client.put(
            "/api/users/update", json={**user, "user_id": user_id, "country": "Lebanon"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["country"], "Lebanon")

        response = self.client.delete(f"/api/users/delete/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "User deleted successfully")
        self.assertEqual(self.client.get(f"/api/users/{user_id}").status_code, 404)

    def test_bad_requests_and_missing_users(self):
        self.assertEqual(self.client.post("/api/users/add", json={}).status_code, 400)
        self.assertEqual(self.client.post("/api/users/add", data="bad").status_code, 400)
        self.assertEqual(self.client.put("/api/users/update", json={}).status_code, 400)
        self.assertEqual(self.client.get("/api/users/999999").status_code, 404)
        self.assertEqual(self.client.delete("/api/users/delete/999999").status_code, 404)


if __name__ == "__main__":
    unittest.main()
