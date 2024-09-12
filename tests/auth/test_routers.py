import pytest
from httpx import AsyncClient



async def test_root(ac: AsyncClient, db_setup_teardown):
    user_data_test = {
        "username": "David",
        "email": "davi.lol@gmail.com",
        "password": "qwertyuiop[]"
    }

    response = await ac.post("/auth/register/", json=user_data_test)

    assert response.status_code == 201
    assert response.json().get("username") == user_data_test["username"]
    assert response.json().get("email") == user_data_test["email"]



async def test_login(ac: AsyncClient, db_setup_teardown):
    user_data_test = {
        "username": "David",
        "email": "davi.lol@gmail.com",
        "password": "qwertyuiop[]"
    }

    response = await ac.post("/auth/register/", json=user_data_test)

    assert response.status_code == 201

    response = await ac.post("/auth/login/", json=user_data_test)

    assert response.status_code == 200, f"{response.json()}"
    assert response.json()['access_token']
    assert response.json()['refresh_token']


async def test_refresh(ac: AsyncClient, db_setup_teardown):
    user_data_test = {
        "username": "David",
        "email": "davi.lol@gmail.com",
        "password": "qwertyuiop[]"
    }
    # create user
    response = await ac.post("/auth/register/", json=user_data_test)

    assert response.status_code == 201

    # login user

    response = await ac.post("/auth/login/", json=user_data_test)

    assert response.status_code == 200
    refresh_token = response.json()["refresh_token"]

    # refresh token
    response = await ac.get("/auth/refresh/", headers={
        "Authorization": f"Bearer {refresh_token}"
    })

    assert response.status_code == 200
    assert response.json()["access"]
