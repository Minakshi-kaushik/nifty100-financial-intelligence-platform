from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


# =====================================================
# Get Screener Results
# =====================================================


def test_screener():

    response = client.get("/api/v1/screener")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# =====================================================
# ROE Filter
# =====================================================


def test_screener_roe():

    response = client.get("/api/v1/screener?min_roe=15")

    assert response.status_code == 200


# =====================================================
# Sector Filter
# =====================================================


def test_screener_sector():

    response = client.get("/api/v1/screener?sector=Financials")

    assert response.status_code == 200


# =====================================================
# Market Cap Filter
# =====================================================


def test_market_cap_filter():

    response = client.get("/api/v1/screener?market_cap_category=Large Cap")

    assert response.status_code == 200


# =====================================================
# Multiple Filters
# =====================================================


def test_multiple_filters():

    response = client.get("/api/v1/screener?sector=Financials&min_roe=10")

    assert response.status_code == 200


# =====================================================
# Invalid Sector
# =====================================================


def test_invalid_sector():

    response = client.get("/api/v1/screener?sector=INVALID")

    assert response.status_code == 200

    assert response.json() == []
