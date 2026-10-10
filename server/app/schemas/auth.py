from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserMeResponse


class AuthCodeRequest(BaseModel):
    email: EmailStr


class AuthCodeVerifyRequest(BaseModel):
    email: EmailStr
    code: str = Field(pattern=r"^\d{6}$")


class AuthMessageResponse(BaseModel):
    message: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthVerifyResponse(AuthTokenResponse):
    user: UserMeResponse
