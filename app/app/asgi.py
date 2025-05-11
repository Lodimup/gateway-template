import os
from contextlib import asynccontextmanager

from brokers import faststream_broker
from django.core.asgi import get_asgi_application
from starlette.applications import Starlette
from starlette.routing import Mount

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")


@asynccontextmanager
async def lifespan(app):
    await faststream_broker.start()
    try:
        yield
    finally:
        await faststream_broker.close()


application = Starlette(
    routes=(Mount("/", get_asgi_application()),),
    lifespan=lifespan,
)
