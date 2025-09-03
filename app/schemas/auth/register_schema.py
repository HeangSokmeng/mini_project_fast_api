from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(None, max_length=100)
    role_name: str = Field(default="staff")  # Default role


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    message: str
