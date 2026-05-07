from typing import List
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator
import os

from app import services
from app.schema import (
    UserIn, UserOut, BaseResponse, UserListOut, 
    ErrorResponse, HealthStatus, ReadinessStatus
)

# Initialize app
app = FastAPI(
    title="FastAPI User Management",
    description="Complete CRUD API with monitoring and security",
    version="1.0.0"
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Exception handlers
@app.exception_handler(services.UserNotFoundError)
async def user_not_found_handler(request: Request, exc: services.UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "User Not Found",
            "detail": str(exc),
            "status_code": 404
        }
    )

@app.exception_handler(services.DuplicateEmailError)
async def duplicate_email_handler(request: Request, exc: services.DuplicateEmailError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Duplicate Email",
            "detail": str(exc),
            "status_code": 409
        }
    )

@app.exception_handler(services.ValidationError)
async def validation_error_handler(request: Request, exc: services.ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": str(exc),
            "status_code": 422
        }
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "detail": "Too many requests. Please try again later.",
            "status_code": 429
        }
    )

# Health & Readiness endpoints
@app.get("/health", response_model=HealthStatus, tags=["Health"])
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Liveness probe - is the app running?"""
    return HealthStatus(
        status="healthy",
        environment=os.getenv("ENVIRONMENT", "production")
    )

@app.get("/ready", response_model=ReadinessStatus, tags=["Health"])
@limiter.limit("100/minute")
async def readiness_check(request: Request):
    """Readiness probe - can the app serve requests?"""
    try:
        # Verify data file is accessible
        services.read_usersdata()
        return ReadinessStatus(
            ready=True,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"ready": False, "timestamp": datetime.utcnow().isoformat()}
        )

@app.get("/status", tags=["Health"])
@limiter.limit("100/minute")
async def status_check(request: Request):
    """Get full app status with metrics"""
    try:
        total_users = services.get_total_users()
        return {
            "status": "running",
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": {
                "total_users": total_users,
                "environment": os.getenv("ENVIRONMENT", "production")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Index endpoint
@app.get("/", tags=["Welcome"])
@limiter.limit("1000/minute")
async def index(request: Request):
    """Welcome endpoint"""
    return {"message": "Hello from FastAPI ;)", "version": "1.0.0"}

# CRUD endpoints
@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["Users"])
@limiter.limit("100/minute")
async def create_user(request: Request, user: UserIn):
    """Create a new user"""
    try:
        created_user = services.add_userdata(user.dict())
        return created_user
    except services.DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/users", response_model=UserListOut, tags=["Users"])
@limiter.limit("500/minute")
async def get_users(request: Request):
    """Get all users"""
    try:
        users = services.get_all_users()
        return UserListOut(data=users, count=len(users))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/{user_id}", response_model=UserOut, tags=["Users"])
@limiter.limit("500/minute")
async def get_user(request: Request, user_id: int):
    """Get a specific user by ID"""
    try:
        user = services.get_user_by_id(user_id)
        return user
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/users/{user_id}", response_model=UserOut, tags=["Users"])
@limiter.limit("100/minute")
async def update_user(request: Request, user_id: int, user: UserIn):
    """Update a user by ID"""
    try:
        updated_user = services.update_user(user_id, user.dict())
        return updated_user
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except services.DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete("/users/{user_id}", response_model=BaseResponse, tags=["Users"])
@limiter.limit("100/minute")
async def delete_user(request: Request, user_id: int):
    """Delete a user by ID"""
    try:
        services.delete_user(user_id)
        return BaseResponse(success=True, message=f"User {user_id} deleted successfully")
    except services.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
