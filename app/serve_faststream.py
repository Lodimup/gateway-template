import sys

if "bin/faststream" in sys.argv[0]:
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()


from appfaststream.routes.demo import router as demo_router
from brokers import faststream_broker
from faststream import FastStream

faststream_broker.include_routers(demo_router)

app = FastStream(faststream_broker)
