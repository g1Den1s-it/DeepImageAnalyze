import base64
import io

import pytest
from httpx import AsyncClient


async def test_create_report(ac: AsyncClient, db_setup_teardown):
    # create test user
    user_data_test = {
        "username": "David",
        "email": "davi.lol@gmail.com",
        "password": "qwertyuiop[]"
    }

    user_response = await ac.post("/auth/register/", json=user_data_test)
    assert user_response.status_code == 201
    user_response = await ac.post("/auth/login/", json=user_data_test)

    # create report of user
    report_test_data = {
        "title": "test report",
    }

    res = await ac.post("/api/reports/create/",
                        data=report_test_data,
                        files={"image": ('tt.jpg', open("/home/g1den1s/python/fastApi/deep_image_analyze/media/images/tt.jpg", "rb"))},
                        headers={
                            "Authorization": f"Bearer {user_response.json()['access_token']}",
                        })

    assert res.status_code == 201
    assert len(res.json()) == 5
    assert res.json()['title'] == report_test_data['title']


async def test_list_reports(ac: AsyncClient, db_setup_teardown):
    # create user
    user_data_test = {
        "username": "David",
        "email": "davi.lol@gmail.com",
        "password": "qwertyuiop[]"
    }

    user_response = await ac.post("/auth/register/", json=user_data_test)
    assert user_response.status_code == 201
    user_response = await ac.post("/auth/login/", json=user_data_test)

    # get list
    res = await ac.get("/api/reports/",
                 headers={
                     "Authorization": f"Bearer {user_response.json()['access_token']}"
                 })

    assert res.status_code == 200
    assert res.json() == []


async def test_detail_report(ac: AsyncClient, db_setup_teardown):
    # create user
    user_data_test = {
        "username": "David",
        "email": "davi.lol@gmail.com",
        "password": "qwertyuiop[]"
    }

    user_response = await ac.post("/auth/register/", json=user_data_test)
    assert user_response.status_code == 201
    user_response = await ac.post("/auth/login/", json=user_data_test)

    # create report of user
    report_test_data = {
        "title": "test report",
    }

    res = await ac.post("/api/reports/create/",
                        data=report_test_data,
                        files={"image": ('tt.jpg', open("/home/g1den1s/python/fastApi/deep_image_analyze/media/images/tt.jpg", "rb"))},
                        headers={
                            "Authorization": f"Bearer {user_response.json()['access_token']}",
                        })

    assert res.status_code == 201
    # get current report

    current_res = await ac.get(f"/api/reports/{res.json()['id']}/",
                               headers={
                                   "Authorization": f"Bearer {user_response.json()['access_token']}"
                               })

    assert current_res.status_code == 200
    assert len(current_res.json()) == 5
    assert current_res.json()['title'] == report_test_data['title']
