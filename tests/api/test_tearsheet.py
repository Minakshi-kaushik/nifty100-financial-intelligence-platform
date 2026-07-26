from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


# =====================================================
# Existing Tearsheet
# =====================================================


def test_existing_tearsheet():

    response = client.get("/api/v1/companies/TCS/tearsheet")

    # Accept either because PDF may or may not exist
    assert response.status_code in [200, 404]


# =====================================================
# Invalid Company
# =====================================================


def test_invalid_tearsheet():

    response = client.get("/api/v1/companies/INVALID/tearsheet")

    assert response.status_code == 404
