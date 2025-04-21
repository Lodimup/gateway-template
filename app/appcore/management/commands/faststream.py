import asyncio

from django.core.management.base import BaseCommand
from serve_faststream import app as faststream_app


class Command(BaseCommand):
    help = "Start FastStream consumer"

    def handle(self, *args, **options):
        asyncio.run(faststream_app.run())
