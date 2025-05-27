"""
FastAPI application for serving websocket connections.
"""

import sys
from contextlib import asynccontextmanager

import aio_pika
from brokers import faststream_broker

from app.app_settings import APP_SETTINGS

if "bin/fastapi" in sys.argv[0]:
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()

from appdemo.fastapi_routes.demo import router as demo_router
from apprealtime.fastapi_routes.electric import router as electric_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app):
    await faststream_broker.start()
    app.state.aio_pika_connection = await aio_pika.connect_robust(
        APP_SETTINGS.FAST_STREAM_BROKER_URL
    )
    try:
        yield
    finally:
        await faststream_broker.close()
        await app.state.aio_pika_connection.close()


app = FastAPI(root_path="/ws", lifespan=lifespan)
app.include_router(demo_router, prefix="/demo", tags=["demo"])
app.include_router(electric_router, prefix="/electric", tags=["electric"])
