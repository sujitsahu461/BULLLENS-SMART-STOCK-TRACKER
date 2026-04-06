import pandas as pd

from bulllens.routes import auth_routes, ml_routes, stock_routes
from bulllens.ml_model import vision_model
from bulllens.conftest import FakeCursor, fake_db_cursor


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "BullLens API"}


def test_root_endpoint_serves_index(client):
    response = client.get("/")

    assert response.status_code == 200


def test_login_success_sets_session_cookies(client, monkeypatch):
    password_hash = auth_routes.hash_password("demo1234")
    user = {
        "user_id": 7,
        "username": "demo",
        "email": "demo@example.com",
        "password_hash": password_hash,
    }
    monkeypatch.setattr(auth_routes, "get_user_by_username", lambda username: user)

    response = client.post("/login", json={"username": "demo", "password": "demo1234"})

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "username": "demo", "user_id": 7}
    assert response.cookies.get("session_user_id") == "7"
    assert response.cookies.get("session_username") == "demo"


def test_login_rejects_invalid_password(client, monkeypatch):
    password_hash = auth_routes.hash_password("demo1234")
    monkeypatch.setattr(
        auth_routes,
        "get_user_by_username",
        lambda username: {
            "user_id": 7,
            "username": "demo",
            "email": "demo@example.com",
            "password_hash": password_hash,
        },
    )

    response = client.post("/login", json={"username": "demo", "password": "wrong"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_register_rejects_duplicate_username(client, monkeypatch):
    monkeypatch.setattr(auth_routes, "get_user_by_username", lambda username: {"user_id": 1, "username": username})

    response = client.post(
        "/register",
        json={"username": "demo", "email": "demo@example.com", "password": "password123"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists"


def test_register_creates_user(client, monkeypatch):
    cursor = FakeCursor(lastrowid=42)
    monkeypatch.setattr(auth_routes, "get_user_by_username", lambda username: None)
    monkeypatch.setattr(auth_routes, "get_db_cursor", lambda commit=True: fake_db_cursor(cursor))

    response = client.post(
        "/register",
        json={"username": "newuser", "email": "newuser@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == 42
    assert response.json()["username"] == "newuser"


def test_root_redirects_new_users_to_register(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/register"


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_authenticated_user_can_open_dashboard(client):
    response = client.get(
        "/dashboard",
        cookies={"session_user_id": "5", "session_username": "demo"},
    )

    assert response.status_code == 200
    assert "demo" in response.text


def test_stock_data_returns_history(client, patch_stock_ticker):
    response = client.get("/api/stock-data/RELIANCE")

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "RELIANCE"
    assert payload["latest_price"] == 104.0
    assert payload["change_pct"] == 4.0
    assert len(payload["history"]) == 5
    assert payload["history"][0]["date"] == "2025-01-01"


def test_stock_data_rejects_unknown_symbol(client, monkeypatch):
    empty_history = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
    monkeypatch.setattr(
        stock_routes.yf,
        "Ticker",
        lambda symbol, session=None: type(
            "TickerStub",
            (),
            {"history": lambda self, period="1mo": empty_history.copy()},
        )(),
    )

    response = client.get("/api/stock-data/UNKNOWN")

    assert response.status_code == 400
    assert response.json()["detail"] == "No data found for symbol UNKNOWN"


def test_watchlist_returns_live_prices(client, monkeypatch):
    rows = [[{"watchlist_id": 9, "symbol": "TCS", "company_name": "Tata", "added_at": "2025-01-05 10:00:00"}]]
    cursor = FakeCursor(fetchall_results=rows)
    monkeypatch.setattr(stock_routes, "get_db_cursor", lambda commit=True: fake_db_cursor(cursor))
    monkeypatch.setattr(stock_routes, "get_stock_latest_price", lambda symbol: (4025.5, 1.23))

    response = client.get("/api/watchlist", params={"user_id": 1})

    assert response.status_code == 200
    assert response.json() == [
        {
            "watchlist_id": 9,
            "symbol": "TCS",
            "company_name": "Tata",
            "latest_price": 4025.5,
            "change_pct": 1.23,
            "added_at": "2025-01-05 10:00:00",
        }
    ]


def test_add_watchlist_creates_entry(client, monkeypatch, stock_history):
    cursor = FakeCursor(fetchone_results=[{"stock_id": 11}], lastrowid=21)
    monkeypatch.setattr(stock_routes, "get_db_cursor", lambda commit=True: fake_db_cursor(cursor))
    monkeypatch.setattr(stock_routes.yf, "Ticker", lambda symbol, session=None: type("TickerStub", (), {"history": lambda self, period="1d": stock_history.copy()})())

    response = client.post(
        "/api/add-watchlist",
        params={"user_id": 1},
        json={"symbol": "TCS", "company_name": "Tata Consultancy Services"},
    )

    assert response.status_code == 201
    assert response.json()["watchlist_id"] == 21
    assert response.json()["stock_id"] == 11
    assert response.json()["symbol"] == "TCS"


def test_volatility_predict_returns_model_output(client, monkeypatch):
    monkeypatch.setattr(
        ml_routes,
        "predict_volatility",
        lambda symbol, horizon: {
            "predicted_volatility": 0.1578,
            "cv_score": 0.0412,
            "unit": "percentage",
        },
    )

    response = client.post("/ml/volatility-predict", json={"symbol": "RELIANCE", "horizon": 10})

    assert response.status_code == 200
    assert response.json() == {
        "symbol": "RELIANCE",
        "horizon": 10,
        "predicted_volatility": 0.1578,
        "cv_score": 0.0412,
        "unit": "percentage",
    }


def test_price_predict_returns_prediction(client, monkeypatch):
    monkeypatch.setattr(
        ml_routes,
        "predict_price",
        lambda symbol, horizon: {
            "predicted_price": 2550.45,
            "confidence_interval": [2500.0, 2600.9],
            "model_used": "linear_regression",
        },
    )

    response = client.post("/ml/price-predict", json={"symbol": "RELIANCE", "horizon": 5})

    assert response.status_code == 200
    assert response.json() == {
        "symbol": "RELIANCE",
        "predicted_price": 2550.45,
        "confidence_interval": [2500.0, 2600.9],
        "horizon_days": 5,
        "model_used": "linear_regression",
    }


def test_vision_predict_requires_image(client):
    response = client.post("/ml/vision-predict")

    assert response.status_code == 400
    assert "No image provided" in response.json()["detail"]


def test_vision_predict_accepts_json_base64(client, monkeypatch):
    monkeypatch.setattr(
        vision_model,
        "run_yolo_inference",
        lambda image_bytes: {
            "detections": 1,
            "result_image_url": "/static/ml_preds/test.png",
            "detections_list": [{"label": "trendline", "confidence": 0.91}],
        },
    )

    response = client.post(
        "/ml/vision-predict",
        json={"image_data": "data:image/png;base64,aGVsbG8="},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["detections"] == 1
    assert response.json()["result_image_url"] == "/static/ml_preds/test.png"


def test_legacy_ml_predict_endpoint_still_works(client, monkeypatch):
    monkeypatch.setattr(
        vision_model,
        "run_yolo_inference",
        lambda image_bytes: {
            "detections": 2,
            "result_image_url": "/static/ml_preds/legacy.png",
            "detections_list": [{"label": "breakout", "confidence": 0.88}],
        },
    )

    response = client.post(
        "/ml/api/ml-predict",
        json={"image_data": "data:image/png;base64,aGVsbG8="},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["detections"] == 2
