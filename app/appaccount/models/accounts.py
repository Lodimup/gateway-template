import uuid

from appcore.models.commons import BaseAutoDate, BaseUUID
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extending the default Django user model.
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    google_uid = models.CharField(max_length=255, null=True, default=None)


class UserProfile(BaseUUID, BaseAutoDate):
    """
    Model for storing user profiles.
    """

    GENDER_CHOICES = [
        ("m", "Male"),
        ("f", "Female"),
        ("n", "Non-binary"),
        ("o", "Other"),
        ("u", "Unknown"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        max_length=255,
        default="",
    )
    last_name = models.CharField(
        max_length=255,
        default="",
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        null=True,
        default=None,
    )
    dob = models.DateField(
        null=True,
        default=None,
    )
