import sys

print(sys.argv[0])
if "bin/fastapi" in sys.argv[0]:
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()

from appdemo.fastapi_routes.demo import router as demo_router
from fastapi import FastAPI

app = FastAPI(root_path="/ws")
app.include_router(demo_router, prefix="/demo", tags=["demo"])
