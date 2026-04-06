"""
Authentication routes for BullLens FastAPI backend.
Provides login, logout, and registration endpoints with bcrypt password hashing.
Session cookies expire on browser close.
"""

import re

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, field_validator
import bcrypt

try:
    from ..database import get_db_cursor
except ImportError:  # pragma: no cover - script execution fallback
    from database import get_db_cursor

router = APIRouter()


# ============================================================================
# Pydantic Models
# ============================================================================

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value):
            raise ValueError("Invalid email address")
        return value


class AuthResponse(BaseModel):
    status: str
    username: str
    user_id: int


# ============================================================================
# Helper Functions
# ============================================================================

def get_user_by_username(username: str) -> dict | None:
    """Fetch user from database by username."""
    try:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT user_id, username, email, password_hash FROM users WHERE username = %s",
                (username,)
            )
            return cursor.fetchone()
    except Exception:
        return None


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with 12 rounds."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


# ============================================================================
# Auth Endpoints
# ============================================================================

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, response: Response):
    """
    Authenticate user and create session.
    
    Args:
        request: LoginRequest with username and password
        response: FastAPI Response to set session cookie
    
    Returns:
        AuthResponse with user details
    
    Raises:
        HTTPException 401: Invalid credentials
    """
    # Fetch user from database
    user = get_user_by_username(request.username)
    
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Set session cookie (expires on browser close - max_age not set or set to session)
    response.set_cookie(
        key="session_user_id",
        value=str(user["user_id"]),
        httponly=True,
        secure=False,  # Set to True in production over HTTPS
        samesite="lax",
        # max_age=None means session cookie (expires on browser close)
    )
    response.set_cookie(
        key="session_username",
        value=user["username"],
        httponly=False,  # Allow JavaScript to read username
        secure=False,
        samesite="lax",
    )
    
    return {
        "status": "ok",
        "username": user["username"],
        "user_id": user["user_id"]
    }


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing session cookies.
    
    Returns:
        Status message
    """
    response.delete_cookie("session_user_id")
    response.delete_cookie("session_username")
    
    return {"status": "ok", "message": "Logged out"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user account.
    
    Args:
        request: RegisterRequest with username, email, password
    
    Returns:
        User details
    
    Raises:
        HTTPException 409: Username or email already exists
        HTTPException 500: Database error
    """
    # Check if username already exists
    existing_user = get_user_by_username(request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Insert new user
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (request.username, request.email, password_hash)
            )
            user_id = cursor.lastrowid
            
            return {
                "status": "ok",
                "message": "Account created successfully",
                "user_id": user_id,
                "username": request.username
            }
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.get("/me")
async def get_me(username: str = None):
    """
    Get current authenticated user profile.
    
    Args:
        username: Username from session cookie
    
    Returns:
        User profile
    
    Raises:
        HTTPException 401: Not authenticated
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"]
    }
