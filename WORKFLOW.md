# BullLens — Developer Workflow Guide

This document covers the three parallel development tracks, git branching strategy, new-developer onboarding, and the Agent handoff protocol.

---

## 📐 Architecture Overview

```
StockMarketPredictor/
  bulllens/
    routes/          ← Track A (Backend/API)
    ml_model/        ← Track C (Data Science)
    static/ + templates/  ← Track B (Frontend)
    sql/             ← Track A only (schema changes)
  API_CONTRACT.md    ← Maintained by Agent 1; read by Agent 2
```

---

## 🛤️ Three Parallel Tracks

### Track A — Backend / API (`routes/`, `database.py`, `sql/`)

**Owner:** Agent 1 (Backend Engineer)

- Work exclusively in `bulllens/routes/`, `bulllens/database.py`, `bulllens/sql/schema.sql`, and `bulllens/models/`.
- **Never** touch `static/` or `templates/`.
- All database schema changes go through `sql/schema.sql` **only** — no ad-hoc `ALTER TABLE` in sessions.
- Test endpoints with `curl` or `httpx` — do not start a browser.
- Mark an endpoint stable by updating `API_CONTRACT.md`. Tag breaking changes `[BREAKING]`.

**Example curl workflow:**
```bash
# Start server
python bulllens/app.py

# Test an endpoint (auth required — get cookie first)
curl -c cookies.txt -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo_user","password":"demo123"}'

curl -b cookies.txt http://localhost:5000/watchlist
```

---

### Track B — Frontend / SPA (`static/`, `templates/`)

**Owner:** Agent 2 (Frontend Engineer)

- Work exclusively in `bulllens/static/css/style.css`, `bulllens/static/js/app.js`, and `bulllens/templates/`.
- **Never** touch any Python, Flask, database, or ML files.
- Keep `DEV_MODE = true` until Agent 1 marks the corresponding endpoint **stable** in `API_CONTRACT.md`.
- Switch `DEV_MODE = false` only after reading `API_CONTRACT.md` and verifying the response shape matches the `MOCK` object.
- No npm, no bundler, no build step — vanilla HTML/CSS/JS only.
- Chart.js loaded from CDN.

**DEV_MODE workflow:**
```javascript
// To flip mock → live for a single endpoint:
// 1. Read API_CONTRACT.md for the endpoint's response shape
// 2. Verify MOCK slice matches
// 3. Set DEV_MODE = false
// 4. curl the endpoint and compare JSON to MOCK
```

---

### Track C — Data Science / ML (`ml_model/`)

**Owner:** Data Science team

- Work exclusively in `bulllens/ml_model/`.
- Each model must be trainable via CLI **without** starting the Flask server:
  ```bash
  # Train volatility model standalone
  python -c "from bulllens.ml_model.risk_model import train_volatility_model; train_volatility_model(horizon=5)"
  ```
- Artifacts write to `bulllens/ml_model/artifacts/` — this directory is **gitignored**.
- Never commit `.pkl`, `.pt`, or `.pth` files.
- When a new model is production-ready, update the corresponding route in `routes/ml_routes.py` (coordinate with Agent 1).
- Document new model inputs/outputs in `bulllens/ml_model/README.md`.

---

## 🌿 Git Branching Strategy

```
main          ← Always deployable. Only PRs from dev. Protected.
dev           ← Integration branch. All feature PRs target here.
feature/*     ← Track A and B feature work
ml/*          ← Track C model experiments and training scripts
```

| Branch | Purpose | PR targets |
|---|---|---|
| `main` | Production-ready code | — |
| `dev` | Integration (staging) | `main` (after QA) |
| `feature/backend-watchlist` | Track A work | `dev` |
| `feature/frontend-ml-view` | Track B work | `dev` |
| `ml/volatility-v2` | Track C experiments | `dev` |

**Rules:**
1. `main` is always deployable — never push directly.
2. All PRs target `dev`, not `main`.
3. `dev` → `main` happens only after manual QA and passing CI.
4. Squash-merge feature branches to keep `dev` history clean.
5. Tag `[BREAKING]` in the PR description for any change that alters an API contract.

---

## 🖥️ New Developer Setup (Clone to Browser)

```powershell
# 1. Clone
git clone https://github.com/your-org/StockMarketPredictor.git
cd StockMarketPredictor

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 3. Install Python dependencies
pip install -r bulllens\requirements.txt

# 4. Set up MySQL database
mysql -u root -p -e "CREATE DATABASE bulllens_db;"
mysql -u root -p bulllens_db < bulllens\sql\schema.sql

# 5. Configure .env
copy bulllens\.env.example bulllens\.env
# Edit bulllens\.env:
#   DB_HOST=localhost
#   DB_PORT=3306
#   DB_USER=root
#   DB_PASSWORD=yourpassword
#   DB_NAME=bulllens_db
#   SECRET_KEY=dev-secret-change-in-prod

# 6. Start the server
cd bulllens
python app.py

# 7. Open browser
#    http://localhost:5000/login
#    demo_user / demo123

# 8. (Optional) Enable DEV_MODE for frontend-only work
#    In bulllens/static/js/app.js, line 1:
#    const DEV_MODE = true;  ← already set by default
#    You can now work on the UI without any backend running.

# 9. Train the volatility model (first run)
curl -X POST http://localhost:5000/ml/volatility-train \
  -H "Content-Type: application/json" \
  -d '{"horizon":5}' \
  -b cookies.txt
```

---

## 🤝 Handoff Protocol

### Agent 1 → Agent 2 (Backend → Frontend)

1. **When an endpoint is ready**, Agent 1 updates `API_CONTRACT.md`:
   - Method, path, request body schema
   - Success response shape and status codes
   - Error codes and their `error` field values
   - Tag breaking changes: `[BREAKING] Changed /watchlist response shape`
2. Agent 2 **checks `API_CONTRACT.md`** before wiring any endpoint.
3. Agent 2 verifies the `MOCK` slice in `app.js` matches the contract.
4. Agent 2 sets `DEV_MODE = false` for that endpoint only (or globally when all endpoints are stable).

### Agent 2 → Agent 1 (Frontend → Backend)

- Agent 2 never changes Python files. If a new endpoint is needed, open a GitHub issue tagging Agent 1.
- If the mock shape differs from what Agent 1 implemented, Agent 2 must update the `MOCK` object to match `API_CONTRACT.md` (not the other way round).

### Breaking Change Protocol

- Any PR that changes a request/response schema, removes an endpoint, or changes an HTTP status code **must** include `[BREAKING]` in the PR title.
- Agent 1 updates `API_CONTRACT.md` in the same PR.
- Agent 2 reviews and updates `MOCK` in a follow-up PR within the same sprint.

---

## 📋 Day-to-Day Rules

| Rule | Reason |
|---|---|
| Never edit files outside your track | Prevents merge conflicts |
| Always test with `DEV_MODE = true` first | Catches UI bugs without needing backend |
| Schema changes only via `schema.sql` | Keeps schema reproducible |
| Artifacts are gitignored | Model files are too large for git |
| PRs target `dev`, not `main` | `main` stays deployable at all times |
| Write `[BREAKING]` in PR title for contract changes | Alerts Agent 2 to update mocks |

---

*Last updated: March 2026*
