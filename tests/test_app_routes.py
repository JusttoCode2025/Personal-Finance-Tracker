import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
  
def test_budget_page(client):
    response = client.get("/budget")
    assert response.status_code == 200

def test_travel_goal_page(client):
    response = client.get("/travel-goal")
    assert response.status_code == 200

def test_dashboard_page(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
