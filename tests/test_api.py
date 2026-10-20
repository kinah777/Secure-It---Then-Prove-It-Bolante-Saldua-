"""API behaviour tests.

ONE example is written for you. Replace each `assert False` TODO with a real test.
Use the helpers from conftest:  login(client, user, pw) -> token,  auth(token) -> header.
Ask for the `client` fixture by adding it as a parameter (it gives you a fresh DB each time).

Run the suite:   pytest -q
Run one file:    pytest tests/test_api.py -q
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1 -------------------------------------------------------------
def test_register_then_login(client):
    # Register a new user, then log in as that user.
    # Assert login returns 200 AND the access_token looks like a JWT
    # (three dot-separated parts: token.count(".") == 2).
    registration = client.post(
        "/register", json={"username": "newuser", "password": "newpass"}
    )
    assert registration.status_code == 200

    res = client.post(
        "/login", json={"username": "newuser", "password": "newpass"}
    )
    assert res.status_code == 200
    assert res.json()["access_token"].count(".") == 2


# ----- TODO 2 -------------------------------------------------------------
def test_login_wrong_password_is_401(client):
    # Log in as 'alice' with the WRONG password. Assert the status code is 401.
    res = client.post(
        "/login", json={"username": "alice", "password": "wrong-password"}
    )
    assert res.status_code == 401


# ----- TODO 3 -------------------------------------------------------------
def test_create_then_list_own_note(client):
    # Log in as alice, POST a new note, then GET /notes and assert the new
    # note's title appears in the list.
    token = login(client, "alice", "alicepass")
    created = client.post(
        "/notes",
        json={"title": "Test note", "body": "Private body"},
        headers=auth(token),
    )
    assert created.status_code == 200

    listed = client.get("/notes", headers=auth(token))
    assert listed.status_code == 200
    assert any(note["title"] == "Test note" for note in listed.json())
