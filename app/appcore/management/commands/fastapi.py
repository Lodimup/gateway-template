import uvicorn
from django.core.management.base import BaseCommand
from serve_fastapi import app as fastapi_app


class Command(BaseCommand):
    """
    Command to run FastAPI WebSocket server.
    Starting via `fastapi run serve_fastapi.py` is recommended.
    """

    help = "Start FastAPI WebSocket server"

    def handle(self, *args, **options):
        uvicorn.run(fastapi_app, host="0.0.0.0", port=8080)
