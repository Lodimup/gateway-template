# ruff: noqa
"""
Allows you to run a Django shell with the current environment.
"""

###############################################################################
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
###############################################################################
from appaccount.models import User


User.objects.all()
