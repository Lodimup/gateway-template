import httpx
from pydantic import BaseModel


class IUserInfo(BaseModel):
    sub: str
    name: str
    given_name: str
    picture: str
    email: str
    email_verified: bool


def get_userinfo(access_token: str) -> IUserInfo | None:
    """
    Fetches user information from Google using the provided access token.

    Args:
        access_token (str): The OAuth 2.0 access token.

    Returns:
        IUserInfo: A Pydantic model containing user information.
    """

    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    with httpx.Client() as client:
        r = client.get(url, headers=headers)
    if r.status_code == 401:
        return None
    r.raise_for_status()

    return IUserInfo(**r.json())


async def aget_userinfo(access_token: str) -> IUserInfo | None:
    """
    Fetches user information from Google using the provided access token.

    Args:
        access_token (str): The OAuth 2.0 access token.

    Returns:
        IUserInfo: A Pydantic model containing user information.
    """

    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
    if r.status_code == 401:
        return None
    r.raise_for_status()

    return IUserInfo(**r.json())
