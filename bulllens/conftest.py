from contextlib import contextmanager

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from bulllens import app as app_module
from bulllens.routes import stock_routes


class FakeCursor:
    def __init__(self, fetchone_results=None, fetchall_results=None, lastrowid=0, execute_side_effect=None):
        self.fetchone_results = list(fetchone_results or [])
        self.fetchall_results = list(fetchall_results or [])
        self.lastrowid = lastrowid
        self.execute_side_effect = execute_side_effect
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))
        if self.execute_side_effect:
            self.execute_side_effect(query, params)

    def fetchone(self):
        if self.fetchone_results:
            return self.fetchone_results.pop(0)
        return None

    def fetchall(self):
        if self.fetchall_results:
            return self.fetchall_results.pop(0)
        return []


@contextmanager
def fake_db_cursor(cursor):
    yield cursor


def make_history_frame(days=5, start=100.0):
    closes = [start + idx for idx in range(days)]
    dates = pd.date_range("2025-01-01", periods=days, freq="D")
    return pd.DataFrame(
        {
            "Open": closes,
            "High": [value + 1 for value in closes],
            "Low": [value - 1 for value in closes],
            "Close": closes,
            "Volume": [1000 + idx for idx in range(days)],
        },
        index=dates,
    )


class FakeTicker:
    def __init__(self, history_frame):
        self._history_frame = history_frame

    def history(self, period="1mo"):
        return self._history_frame.copy()


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(app_module, "init_db", lambda: None)

    async def fake_provision_demo_account():
        return None

    monkeypatch.setattr(app_module, "provision_demo_account", fake_provision_demo_account)

    with TestClient(app_module.create_app()) as test_client:
        yield test_client


@pytest.fixture
def stock_history():
    return make_history_frame(days=5, start=100.0)


@pytest.fixture
def patch_stock_ticker(monkeypatch, stock_history):
    monkeypatch.setattr(stock_routes.yf, "Ticker", lambda symbol, session=None: FakeTicker(stock_history))
    return stock_history
