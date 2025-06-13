from typing import Literal

from ninja import Field, Schema
from pydantic import EmailStr

PROVIDERS = Literal["google"]


class LoginPostIn(Schema):
    access_token: str
    provider: PROVIDERS


class LoginTrustedPostIn(Schema):
    uid: str
    email: EmailStr | None = Field(None, description="Email of the user")
    provider: PROVIDERS


class LoginPostOut(Schema):
    access_token: str
    expires_in: int
    refresh_token: str
    refresh_token_expires_in: int


class RefreshPostIn(Schema):
    refresh_token: str


class RefreshPostOut(Schema):
    access_token: str
    expires_in: int
    refresh_token: str
