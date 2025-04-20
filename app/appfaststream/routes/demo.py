from appaccount.models.accounts import User
from appdemo.serializers.demos import DemoQueueSchema
from faststream.rabbit import RabbitRouter

router = RabbitRouter()


@router.subscriber("demo")
async def base_handler(message=DemoQueueSchema):
    qs = User.objects.all()
    async for user in qs:
        print(user)
    print(message)
