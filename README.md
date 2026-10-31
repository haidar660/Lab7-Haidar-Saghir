# Lab 7 Python Testing

**Student:** Haidar Saghir  
**Course:** ECE 435L Software Tools Lab

This project extends the Lab 5 Flask and SQLite user API with the Pytest suite required for Lab 7. The file `test_user_Haidar_Saghir.py` contains ten independent tests for database initialization, the five database operations, and the four API operations named in the handout.

## Run the API

From this project folder, use Python 3.9 or newer:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

The server starts at `http://localhost:5000`. Opening `http://localhost:5000/api/users` in a browser shows the users currently stored in the database. On its first run, the app creates `database.db`, creates the `users` table, and adds the specified John Doe user. Python includes `sqlite3`, so it does not need a separate package installation.

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/users` | List all users |
| GET | `/api/users/<user_id>` | Get one user |
| POST | `/api/users/add` | Add a user |
| PUT | `/api/users/update` | Update a user |
| DELETE | `/api/users/delete/<user_id>` | Delete a user |

POST requires `name`, `email`, `phone`, `address`, and `country` as nonempty JSON strings. PUT requires those fields plus a positive integer `user_id`. Both return JSON. Invalid input returns HTTP 400; an unknown user ID returns HTTP 404.

## Run the Postman collection

1. Import `postman/Flask-user-app.postman_collection.json` and `postman/Flask-user-app-local.postman_environment.json` into Postman.
2. Select the **Flask user app local** environment. Its `base_url` variable is `http://localhost:5000`.
3. Start the Flask server and run the collection in order: Add user, Get all users, Get user by ID, Update user, Delete user. Add user saves the new ID to the `user_id` environment variable.
4. Open a request's **Examples** section to inspect its saved response. The examples were captured from the running Flask app with a temporary database.

Each collection run adds and then deletes one sample user. Existing users in `database.db` are left in place.

## Run the Lab 7 tests

```powershell
python -m pytest -v test_user_Haidar_Saghir.py
```

The ten Lab 7 tests use a fresh temporary SQLite database for every test. They verify database creation and initial data, all five database operations, and all four required API operations. The API tests check both HTTP status codes and uploaded or downloaded JSON data. The submitted `database.db` is not modified during testing.

## Moodle submission evidence

The repository includes the [Lab 7 Pytest success image](screenshots/lab7-pytest-passed.png) required for Moodle. It shows all ten required tests passing. The previous [five Postman screenshots](screenshots/README.md) remain included as supporting Lab 5 evidence.
