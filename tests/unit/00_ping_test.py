import pytest
import requests

import time

# pip install pytest requests
def test_ping():
    response = requests.get("http://localhost:8080/ping")

    assert response.status_code == 200


def test_ping_overflow():
    time_start = time.time()

    for _ in range(100):
        response = requests.get("http://localhost:8080/ping")

    time_consumed = time.time() - time_start

    assert time_consumed < 1.0


def test_ping_list():
    response = requests.get("http://localhost:8080/ping/list")

    assert response.status_code == 200



def test_ping_id():
    response = requests.get("http://localhost:8080/ping")

    assert response.status_code == 200

    id = response.json().get("connection", {}).get("id")

    response = requests.get(f"http://localhost:8080/ping/single/{id}")

    assert response.status_code == 200
    assert str(response.json().get("id")) == str(id)