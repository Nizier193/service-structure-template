import pytest
import requests

# pip install pytest requests
def test_ping():
    response = requests.get("http://localhost:8080/ping")

    assert response.status_code == 200