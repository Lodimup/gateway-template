from appaccount.models.auths import Session
from appaccount.serializers.auths import (
    LoginPostIn,
    LoginPostOut,
    LoginTrustedPostIn,
    RefreshPostIn,
    RefreshPostOut,
)
from appaccount.services.auths import BearerTokenAuth, create_session
from appaccount.services.oauth.google import get_userinfo
from appcore.services.auths import ServiceBearerTokenAuth
from ninja.errors import HttpError
from ninja.router import Router

router = Router(tags=["account", "auth"])


@router.post(
    "/login/",
    response={200: LoginPostOut},
    auth=ServiceBearerTokenAuth(),
)
def post_login(request, payload: LoginPostIn):
    """
    Log in using an access token; creates a session and user if not present.
    """
    match payload.provider:
        case "google":
            userinfo = get_userinfo(payload.access_token)
        case _:
            raise HttpError(400, "Unsupported provider")

    if userinfo is None:
        raise HttpError(401, "Invalid access token")

    session = create_session(
        uid=userinfo.sub, provider=payload.provider, email=userinfo.email
    )

    ret = {
        "access_token": session.access_token,
        "expires_in": session.expires_in,
        "refresh_token": session.refresh_token,
        "refresh_token_expires_in": session.refresh_token_expires_in,
    }

    return 200, ret


@router.post(
    "/login-trusted/",
    response={200: LoginPostOut},
    auth=ServiceBearerTokenAuth(),
)
def post_login_trusted(request, payload: LoginTrustedPostIn):
    """
    Login through API. This trust service has validated the user. It creates a session, and a user if not exist.
    """
    session = create_session(
        uid=payload.uid, provider=payload.provider, email=payload.email
    )

    ret = {
        "access_token": session.access_token,
        "expires_in": session.expires_in,
        "refresh_token": session.refresh_token,
        "refresh_token_expires_in": session.refresh_token_expires_in,
    }

    return 200, ret


@router.post(
    "/logout/",
    response={204: None},
    auth=BearerTokenAuth(),
)
def post_logout(request):
    """
    Logout given access_token, session is destroyed.
    """
    request.auth.destroy()

    return 204, None


@router.post(
    "/refresh/",
    response={200: RefreshPostOut, 401: None},
)
def post_refresh(request, payload: RefreshPostIn):
    """
    Refresh access_token using refresh_token.
    """
    session = Session.objects.filter(refresh_token=payload.refresh_token).first()
    if session is None:
        return 401, None
    if session.is_refresh_token_expired():
        session.destroy()
        return 401, None
    session.refresh(refresh_token=payload.refresh_token)
    ret = {
        "access_token": session.access_token,
        "expires_in": session.expires_in,
        "refresh_token": session.refresh_token,
    }

    return 200, ret
