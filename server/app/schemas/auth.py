from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserMeResponse


class AuthCodeRequest(BaseModel):
    email: EmailStr


class AuthCodeVerifyRequest(BaseModel):
    email: EmailStr
    code: str = Field(pattern=r"^\d{6}$")


class AuthRefreshRequest(BaseModel):
    refresh_token: str


class AuthMessageResponse(BaseModel):
    message: str


class AuthAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthTokenResponse(AuthAccessTokenResponse):
    refresh_token: str


class AuthVerifyResponse(AuthTokenResponse):
    user: UserMeResponse
