from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
import jwt
from app.app import app
import pytest
from app.endpoints import users
from app.environment import settings

import sqlite3


client = TestClient(app=app)

test_user = {"username" : "blaze", "email" : "blaze@gmail.com", "password" : "blazebuster1234"}


def clean_up_new_user_created():
    connection = sqlite3.connect(r"C:\Users\blaze\Work Space\Projects\Projects\SkillBranch\Backend\database\skillbranch.db")
    connection.execute("DELETE FROM user WHERE email = ?", (test_user["email"],))
    connection.commit()
    connection.close()


def test_jwt_session_expired_rejection(monkeypatch : pytest.MonkeyPatch):
    clean_up_new_user_created()
    def generate_expired_token(email : str) -> str:
        return jwt.encode(payload={"sub" : test_user["email"], "exp" : datetime.now(timezone.utc) - timedelta(seconds=10)},key=settings.JWT_SECRET_KEY,algorithm=settings.ALGORITHM,)


    monkeypatch.setattr(users, "generate_jwt_token", generate_expired_token)
    response = client.post("/user/signup", json=test_user)
    assert response.status_code == 201

    auth_header = { "accept" : "application/json", "Authorization" : f"Bearer {response.json()["access_token"]}"}


    response = client.get("/skill/skills", headers=auth_header)

    assert response.status_code == 401

    clean_up_new_user_created()

def test_reject_invalid_jwt():
    auth_header = { "accept" : "application/json", "Authorization" : "Bearer 2c0c3ad57eef4438af688b495eac4cda"}


    response = client.get("/skill/skills", headers=auth_header)

    assert response.status_code == 400



    clean_up_new_user_created()