from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_all_sectors():
    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0


def test_sector_companies():
    response = client.get("/api/v1/sectors/Financials/companies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_invalid_sector():
    response = client.get("/api/v1/sectors/INVALID/companies")

    assert response.status_code == 404
