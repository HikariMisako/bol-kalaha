from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_scores():
    response = client.get("/get_scores")
    assert response.status_code == 200


