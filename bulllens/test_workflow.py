from bulllens.routes import auth_routes, stock_routes
from bulllens.conftest import FakeCursor, fake_db_cursor


def test_user_can_login_and_view_watchlist(client, monkeypatch):
    password_hash = auth_routes.hash_password("demo1234")
    monkeypatch.setattr(
        auth_routes,
        "get_user_by_username",
        lambda username: {
            "user_id": 5,
            "username": "demo",
            "email": "demo@example.com",
            "password_hash": password_hash,
        },
    )

    cursor = FakeCursor(
        fetchall_results=[
            [
                {
                    "watchlist_id": 2,
                    "symbol": "INFY",
                    "company_name": "Infosys",
                    "added_at": "2025-01-10 09:30:00",
                }
            ]
        ]
    )
    monkeypatch.setattr(stock_routes, "get_db_cursor", lambda commit=True: fake_db_cursor(cursor))
    monkeypatch.setattr(stock_routes, "get_stock_latest_price", lambda symbol: (1900.0, -0.8))

    login_response = client.post("/login", json={"username": "demo", "password": "demo1234"})
    watchlist_response = client.get("/api/watchlist", params={"user_id": login_response.json()["user_id"]})

    assert login_response.status_code == 200
    assert watchlist_response.status_code == 200
    assert watchlist_response.json()[0]["symbol"] == "INFY"


def test_user_can_add_and_remove_watchlist_entry(client, monkeypatch, stock_history):
    add_cursor = FakeCursor(fetchone_results=[{"stock_id": 13}], lastrowid=99)
    remove_cursor = FakeCursor(fetchone_results=[{"user_id": 1}])
    cursors = [add_cursor, remove_cursor]

    def next_cursor(commit=True):
        return fake_db_cursor(cursors.pop(0))

    monkeypatch.setattr(stock_routes, "get_db_cursor", next_cursor)
    monkeypatch.setattr(
        stock_routes.yf,
        "Ticker",
        lambda symbol, session=None: type("TickerStub", (), {"history": lambda self, period="1d": stock_history.copy()})(),
    )

    add_response = client.post("/api/add-watchlist", params={"user_id": 1}, json={"symbol": "TCS"})
    remove_response = client.delete("/api/remove-watchlist/99", params={"user_id": 1})

    assert add_response.status_code == 201
    assert add_response.json()["watchlist_id"] == 99
    assert remove_response.status_code == 200
    assert remove_response.json()["status"] == "ok"
