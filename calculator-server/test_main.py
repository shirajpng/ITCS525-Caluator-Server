from fastapi.testclient import TestClient
from main import app  # or whatever your app module is
from collections import deque

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# Test cases for the history apis
def test_get_history_empty():
    client.delete("/history")
    r = client.get("/history")
    assert r.status_code == 200
    assert r.json() == []  # Expect an empty list

def test_get_history_with_data():
    client.post("/calculate", params={"expr": "36+36"})
    client.post("/calculate", params={"expr": "1000+555"})
    client.post("/calculate", params={"expr": "10001*555%"})
    
    r = client.get("/history")
    assert r.status_code == 200
    history = r.json()
    assert len(history) == 3
    assert history[0]["expr"] == "10001*555%"

def test_get_limited_history():
    r = client.get("/history?limit=2")
    assert r.status_code == 200
    history = r.json()
    assert len(history) == 2

def test_delete_history():
    client.post("/calculate", params={"expr": "36+36"})
    client.post("/calculate", params={"expr": "1000+555"})
    client.post("/calculate", params={"expr": "10001*555%"})
    
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True

def test_show_history_after_deleteing_distory():
    client.post("/calculate", params={"expr": "36+36"})
    client.post("/calculate", params={"expr": "1000+555"})
    client.post("/calculate", params={"expr": "10001*555%"})
    
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True

    r = client.get("/history")
    assert r.status_code == 200
    assert r.json() == []

def test_delete_history_when_empty():
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True
