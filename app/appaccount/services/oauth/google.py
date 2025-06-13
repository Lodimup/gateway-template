import httpx
from pydantic import BaseModel


class IUserInfo(BaseModel):
    sub: str
    name: str
    given_name: str
    picture: str
    email: str
    email_verified: bool


def get_userinfo(access_token: str) -> IUserInfo:
    """
    Fetches user information from Google using the provided access token.

    Args:
        access_token (str): The OAuth 2.0 access token.

    Returns:
        IUserInfo: A Pydantic model containing user information.
    """

    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = httpx.get(url, headers=headers)
    r.raise_for_status()

    return IUserInfo(**r.json())
