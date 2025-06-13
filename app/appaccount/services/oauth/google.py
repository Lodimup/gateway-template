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
        dict: A dictionary containing user information.
    """

    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = httpx.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch user info: {response.status_code} {response.text}"
        )

    return IUserInfo(**response.json())
