"""
models/watchlist_model.py
=========================
Data-access layer for the watchlist and stocks tables.

All functions open their own connection and close it when done so that
each request is independent. This keeps the code simple for a local
single-user environment; a connection pool can be swapped in later.
"""

try:
    from ..database import get_connection
except ImportError:  # pragma: no cover - script execution fallback
    from database import get_connection


# ---------------------------------------------------------------
# READ
# ---------------------------------------------------------------

def get_all_watchlist(user_id: int = 1) -> list[dict]:
    """
    Return every stock on the watchlist for *user_id*.

    Joins watchlist → stocks to get symbol, company name, exchange,
    and the timestamp when the stock was added.
    """
    sql = """
        SELECT
            w.watchlist_id,
            s.stock_id,
            s.symbol,
            s.company_name,
            s.exchange,
            w.added_at
        FROM watchlist w
        JOIN stocks s ON w.stock_id = s.stock_id
        WHERE w.user_id = %s
        ORDER BY w.added_at DESC
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchall()
    finally:
        conn.close()


# ---------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------

def add_to_watchlist(symbol: str, company_name: str, exchange: str,
                     user_id: int = 1) -> dict:
    """
    Add *symbol* to the watchlist for *user_id*.

    * Inserts the stock into the `stocks` table if it doesn't exist yet
      (INSERT IGNORE keeps the existing row if the symbol is already there).
    * Then inserts a row into `watchlist`.

    Returns a dict with the new watchlist_id, or raises if the stock is
    already on the watchlist.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # 1. Ensure the stock exists in the master table
            cur.execute(
                """
                INSERT IGNORE INTO stocks (symbol, company_name, exchange)
                VALUES (%s, %s, %s)
                """,
                (symbol.upper(), company_name, exchange),
            )

            # 2. Fetch the stock_id (whether just inserted or already there)
            cur.execute(
                "SELECT stock_id FROM stocks WHERE symbol = %s",
                (symbol.upper(),),
            )
            row = cur.fetchone()
            stock_id = row["stock_id"]

            # 3. Add to the watchlist (raises IntegrityError if duplicate)
            cur.execute(
                """
                INSERT INTO watchlist (user_id, stock_id)
                VALUES (%s, %s)
                """,
                (user_id, stock_id),
            )
            watchlist_id = cur.lastrowid
            conn.commit()

        return {"watchlist_id": watchlist_id, "stock_id": stock_id}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------

def remove_from_watchlist(watchlist_id: int, user_id: int | None = None) -> bool:
    """
    Delete the watchlist row with the given *watchlist_id*.

    If *user_id* is supplied, deletion is scoped to that user so one account
    cannot remove another's entry.  Returns True if a row was actually
    deleted, False if not found or not owned by the user.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if user_id is None:
                cur.execute(
                    "DELETE FROM watchlist WHERE watchlist_id = %s",
                    (watchlist_id,),
                )
            else:
                cur.execute(
                    "DELETE FROM watchlist WHERE watchlist_id = %s AND user_id = %s",
                    (watchlist_id, user_id),
                )
            affected = cur.rowcount
            conn.commit()
        return affected > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
