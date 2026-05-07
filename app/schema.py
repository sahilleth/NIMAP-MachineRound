from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator

class UserIn(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    age: int = Field(..., ge=0, le=150)
    
    @validator('first_name', 'last_name')
    def names_alphanumeric(cls, v):
        if not v.replace(' ', '').isalpha():
            raise ValueError('Names must contain only letters and spaces')
        return v.strip()

class UserOut(UserIn):
    id: int

class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int

class UserListOut(BaseModel):
    data: List[UserOut]
    count: int

class HealthStatus(BaseModel):
    status: str
    version: str = "1.0.0"
    environment: str

class ReadinessStatus(BaseModel):
    ready: bool
    timestamp: str