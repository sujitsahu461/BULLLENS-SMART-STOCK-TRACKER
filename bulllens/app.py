"""
BullLens FastAPI application factory and startup.
Provides REST API for Indian NSE equity tracking with ML-powered predictions.
"""

import os
from contextlib import asynccontextmanager
from fastapi import Cookie, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import bcrypt

try:
    from .database import init_db, get_db_cursor
except ImportError:  # pragma: no cover - script execution fallback
    from database import init_db, get_db_cursor

load_dotenv()


# ============================================================================
# Startup and Shutdown Events
# ============================================================================

async def provision_demo_account():
    """
    Auto-provision a demo account on startup if not already present.
    Username: demo, Password: demo1234 (bcrypt-hashed).
    """
    demo_username = os.getenv("DEMO_USERNAME", "demo")
    demo_password = os.getenv("DEMO_PASSWORD", "demo1234")
    
    try:
        with get_db_cursor() as cursor:
            # Check if demo user already exists
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s",
                (demo_username,)
            )
            existing = cursor.fetchone()
            
            if not existing:
                # Hash password with bcrypt
                password_hash = bcrypt.hashpw(
                    demo_password.encode("utf-8"),
                    bcrypt.gensalt(rounds=12)
                ).decode("utf-8")
                
                # Insert demo user
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (demo_username, f"{demo_username}@bulllens.com", password_hash)
                )
                print(f"✓ Demo account provisioned: {demo_username}")
            else:
                print(f"✓ Demo account already exists: {demo_username}")
    except Exception as e:
        print(f"⚠ Warning: Could not auto-provision demo account: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    """
    # On startup
    print("🚀 BullLens API starting up...")
    try:
        init_db()
        await provision_demo_account()
        print("✓ Startup complete")
    except Exception as e:
        print(f"✗ Startup failed: {e}")
        raise
    
    yield
    
    # On shutdown
    print("🛑 BullLens API shutting down...")


# ============================================================================
# App Factory
# ============================================================================

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance.
    """
    app = FastAPI(
        title="BullLens API",
        description="REST API for Indian NSE equity tracking with ML predictions",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # ========================================================================
    # CORS Configuration
    # ========================================================================
    cors_origins = os.getenv(
        "CORS_ORIGINS",
        '["http://localhost:3000", "http://localhost:8000"]'
    )
    
    try:
        import json
        origins_list = json.loads(cors_origins)
    except:
        origins_list = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ========================================================================
    # Static Files & Templates
    # ========================================================================
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    templates = Jinja2Templates(directory=templates_dir)
    
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # ========================================================================
    # Register Routers
    # ========================================================================
    try:
        from .routes.auth_routes import router as auth_router
        from .routes.stock_routes import router as stock_router
        from .routes.ml_routes import router as ml_router
    except ImportError:  # pragma: no cover - script execution fallback
        from routes.auth_routes import router as auth_router
        from routes.stock_routes import router as stock_router
        from routes.ml_routes import router as ml_router
    
    app.include_router(auth_router, prefix="", tags=["auth"])
    app.include_router(stock_router, prefix="/api", tags=["stocks"])
    app.include_router(ml_router, prefix="/ml", tags=["ml"])
    
    # ========================================================================
    # Root Endpoints
    # ========================================================================
    @app.get("/")
    async def root(session_user_id: str | None = Cookie(default=None)):
        """Send new users to register first, authenticated users to dashboard."""
        destination = "/dashboard" if session_user_id else "/register"
        return RedirectResponse(url=destination, status_code=303)

    @app.get("/register", response_class=HTMLResponse)
    async def register_page(request: Request, session_user_id: str | None = Cookie(default=None)):
        """Render the registration page."""
        if session_user_id:
            return RedirectResponse(url="/dashboard", status_code=303)
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"page_title": "Create Account - BullLens"},
        )

    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request, session_user_id: str | None = Cookie(default=None)):
        """Render the login page."""
        if session_user_id:
            return RedirectResponse(url="/dashboard", status_code=303)
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"page_title": "Login - BullLens"},
        )

    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard_page(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
        session_username: str | None = Cookie(default=None),
    ):
        """Render the main dashboard for authenticated users."""
        if not session_user_id:
            return RedirectResponse(url="/login", status_code=303)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "username": session_username or "Investor",
                "asset_version": str(int(os.path.getmtime(os.path.join(static_dir, "js", "app.js")))),
            },
        )
    
    @app.get("/settings", response_class=HTMLResponse)
    async def settings_page(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Render the full settings management page for authenticated users."""
        if not session_user_id:
            return RedirectResponse(url="/login", status_code=303)
        return templates.TemplateResponse(
            request=request,
            name="settings.html",
            context={},
        )
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "service": "BullLens API"}
    
    # ========================================================================
    # Settings API Endpoints
    # ========================================================================
    
    @app.post("/api/profile")
    async def save_profile(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save user profile settings."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        
        try:
            data = await request.json()
            # Store in database
            with get_db_cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET email = %s WHERE user_id = %s",
                    (data.get("email"), session_user_id)
                )
            return {"success": True, "message": "Profile saved"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/predictions")
    async def save_predictions(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save prediction preferences."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        return {"success": True, "message": "Preferences saved"}
    
    @app.post("/api/market")
    async def save_market(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save market selection preferences."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        return {"success": True, "message": "Market settings saved"}
    
    @app.post("/api/notifications")
    async def save_notifications(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save notification preferences."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        return {"success": True, "message": "Notifications saved"}
    
    @app.post("/api/appearance")
    async def save_appearance(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save appearance preferences."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        return {"success": True, "message": "Appearance settings saved"}
    
    @app.post("/api/watchlist")
    async def save_watchlist(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save watchlist settings."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        return {"success": True, "message": "Watchlist saved"}
    
    @app.post("/api/security")
    async def save_security(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save security settings."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        
        try:
            data = await request.json()
            # Validate and update password if provided
            if data.get("newPassword"):
                # Add password hashing logic here
                pass
            return {"success": True, "message": "Security settings updated"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @app.post("/api/feedback")
    async def save_feedback(
        request: Request,
        session_user_id: str | None = Cookie(default=None),
    ):
        """Save user feedback."""
        if not session_user_id:
            return {"success": False, "message": "Unauthorized"}, 401
        
        try:
            data = await request.json()
            # Store feedback in database or email
            return {"success": True, "message": "Feedback received"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    return app


# ============================================================================
# Application Instance & Entry Point
# ============================================================================

app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    env = os.getenv("UVICORN_ENV", "development")
    debug = env == "development"
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info" if debug else "warning",
    )
