from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)
# Test cases for the FastAPI application
# These tests cover the root endpoint and the predict endpoint, including valid and invalid inputs.

# Test for the root endpoint
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the NLP Review Pipeline API!"}

# Test for the predict endpoint with valid data
def test_predict_endpoint():
    response = client.post("/predict", json={
        "verified": True,
        "reviewerID": "test_user",
        "asin": "B001",
        "reviewText": "Great product",
        "summary": "Loved it",
        "overall": 5.0
    })
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probability" in response.json()

# Test for the predict endpoint with invalid data types
def test_predict_endpoint_invalid_data():
    response = client.post("/predict", json={
        "verified": "not_a_boolean",
        "reviewerID": 12345,
        "asin": "B001",
        "reviewText": "Great product",
        "summary": "Loved it",
        "overall": 5.0
    })
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json() == {
        "detail": [
            {
                "input": "not_a_boolean",
                "loc": ["body", "verified"],
                "msg": "Input should be a valid boolean, unable to interpret input",
                "type": "bool_parsing"
            },
            {
                "input": 12345,
                "loc": ["body", "reviewerID"],
                "msg": "Input should be a valid string",
                "type": "string_type"
            }
        ]
    }

# Test for the predict endpoint with missing fields
def test_predict_endpoint_missing_fields():
    response = client.post("/predict", json={
        "verified": True,
        "reviewerID": "test_user",
        "asin": "B001",
        # Missing reviewText, summary, and overall
    })
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "reviewText"],
                "msg": "Field required"
            },
            {
                "type": "missing",
                "loc": ["body", "summary"],
                "msg": "Field required"
            },
            {
                "type": "missing",
                "loc": ["body", "overall"],
                "msg": "Field required"
            }
        ]
    }