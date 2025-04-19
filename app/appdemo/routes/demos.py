from appaccount.models.accounts import User
from appaccount.services.auths import ABearerTokenAuth
from appdemo.serializers.demos import SvActFormFileDemoPostIn
from ninja import Form, ModelSchema, Router, UploadedFile

router = Router(tags=["demos"])


@router.post(
    "/form-action-upload/",
    response={204: None},
)
def post_form_action_upload(
    request,
    payload: Form[SvActFormFileDemoPostIn],
    file: UploadedFile | None = None,
):
    """
    Demo for uploading file using multipart/form-data.
    See: http://localhost:3000/demo/form-action-upload
    """
    print(payload.name)
    print(type(file), file)
    return 204, None


class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ["password"]


@router.get(
    "/authenticated-sync-route/",
    response=UserSchema,
)
def get_authenticated_sync_route(request):
    return request.auth.user


@router.get(
    "/authenticated-async-route/",
    response=UserSchema,
    auth=ABearerTokenAuth(),
)
async def get_authenticated_async_route(request):
    """
    Sample for ABearerTokenAuth and further queries in async route.
    """
    session = request.auth
    user = (
        await User.objects.filter(id=session.user_id)
        .prefetch_related("groups")
        .prefetch_related("user_permissions")
        .afirst()
    )
    return user
