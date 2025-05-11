import os
from contextlib import asynccontextmanager

from django.core.asgi import get_asgi_application
from faststream.rabbit import RabbitBroker
from starlette.applications import Starlette
from starlette.routing import Mount

from app.app_settings import APP_SETTINGS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

broker = RabbitBroker(APP_SETTINGS.FAST_STREAM_BROKER_URL)


@asynccontextmanager
async def lifespan(app):
    await broker.start()
    try:
        yield
    finally:
        await broker.close()


application = Starlette(
    routes=(Mount("/", get_asgi_application()),),
    lifespan=lifespan,
)
