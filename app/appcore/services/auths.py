from typing import Literal

from ninja.security import HttpBearer

from app.app_settings import APP_SETTINGS


class ServiceBearerTokenAuth(HttpBearer):
    """Used to authenticate NextJS's server side calls"""

    async def authenticate(self, request, token) -> Literal[True] | None:
        """This is a function to authenticate using token.
        Args:
            request (Request): request object
            token (str): token

        Returns:
            Session | None: session object if authenticated, None otherwise
        """
        if token == APP_SETTINGS.SERVICE_TOKEN:
            return True

        return None
