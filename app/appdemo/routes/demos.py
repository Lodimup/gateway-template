from appaccount.models.accounts import User
from appaccount.services.auths import ABearerTokenAuth
from appdemo.serializers.demos import DemoQueueSchema, SvActFormFileDemoPostIn
from ninja import Form, ModelSchema, Router, Schema, UploadedFile

from app.asgi import broker

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
    # user is already available but select user again to prefetch to be used in UserSchema
    user = (
        await User.objects.filter(id=session.user_id)
        .prefetch_related("groups")
        .prefetch_related("user_permissions")
        .afirst()
    )
    return user


class ProduceFastStreamPostIn(Schema):
    """
    Schema for the produce fast stream endpoint.
    """

    message: str


@router.post("produce-fast-stream/", auth=None)
async def post_produce_fast_stream(
    request,
    payload: ProduceFastStreamPostIn,
):
    """
    Endpoint to produce a message to the fast stream in the demo queue.
    Note: depending on the security requirements, send UUID linked to data or actual payload.
    """
    await broker.publish(DemoQueueSchema(**payload.model_dump()), "demo")

    return {"message": "Message produced to fast stream"}
