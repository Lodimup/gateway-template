import sys

if "bin/faststream" in sys.argv[0]:
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()


from appfaststream.routes.demo import router as demo_router
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.app_settings import APP_SETTINGS

broker = RabbitBroker(APP_SETTINGS.FAST_STREAM_BROKER_URL)
broker.include_routers(demo_router)

app = FastStream(broker)
