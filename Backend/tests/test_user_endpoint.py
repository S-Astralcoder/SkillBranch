from fastapi.testclient import TestClient
from app.app import app
import pytest

import sqlite3


client = TestClient(app=app)

test_user = {
    "username": "blaze",
    "email": "blaze@gmail.com",
    "password": "blazebuster1234",
}


def clean_up_new_user_created():
    connection = sqlite3.connect(
        r"C:\Users\blaze\Work Space\Projects\Projects\SkillBranch\Backend\database\skillbranch.db"
    )
    connection.execute("DELETE FROM user WHERE email = ?", (test_user["email"],))
    connection.commit()
    connection.close()


def test_create_new_user_creation():
    clean_up_new_user_created()
    response = client.post(url="/user/signup", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, dict)
    assert data.keys() == {"access_token", "token_type"}
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_reject_duplicate_email_user_creation():
    response = client.post(url="/user/signup", json=test_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "The User Already Exists"}


def test_jwt_token_generation_after_signup():
    response = client.post(
        "/user/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data.keys() == {"access_token", "token_type"}
    assert data["access_token"]
    assert data["token_type"] == "bearer"


# Happy tests done


@pytest.mark.parametrize(
    ("invalid_user"),
    [
        {"username": "blaze", "email": "blaze@gmail.com", "password": ""},
        {"username": "blaze", "email": "blaze", "password": "blazebuster1234"},
        {"username": "", "email": "blaze@gmail.com", "password": "blazebuster1234"},
        {"username": "", "email": "", "password": ""},
        {"username": "blaze", "email": "blaze@gmail.com", "code": "blazebuster1234"},
        {
            "username": "blaze" * 100,
            "email": "blaze@gmail.com",
            "password": "blazebuster1234",
        },
        {
            "username": "blaze" * 100,
            "email": "blaze@gmail.com" * 200,
            "password": "blazebuster1234" * 200,
        },
    ],
)
def test_reject_invalid_user_signup(invalid_user: dict[str, str]):
    response = client.post(url="/user/signup", json=invalid_user)
    assert response.status_code == 422


def test_reject_issue_jwt_for_non_registered_user():
    response = client.post(
        "/user/login",
        data={"username": "test@my.com", "password": test_user["password"]},
    )
    assert response.status_code == 404


def test_reject_issue_jwt_for_invalid_password_user():
    response = client.post(
        "/user/login", data={"username": test_user["email"], "password": "password123"}
    )
    assert response.status_code == 401


def test_reject_non_email_in_username_field():
    response = client.post(
        "/user/login",
        data={"username": test_user["username"], "password": "password123"},
    )
    print(response.json())
    assert response.status_code == 406

    clean_up_new_user_created()
