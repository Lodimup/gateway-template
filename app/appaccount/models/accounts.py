import uuid

from appcore.models.commons import BaseAutoDate, BaseUUID
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extending the default Django user model.
    id: UUID
    google_uid: Google user ID TODO: Use Account Model, use can have multiple accounts from multiple providers
    realtime_exchange: rabbitmq exchange id for real time application
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    realtime_exchange = models.UUIDField(default=uuid.uuid4)


class Account(BaseUUID, BaseAutoDate):
    """
    See: https://github.com/nextauthjs/next-auth/blob/24b82d9872aa8230aa723ab7abe8e4a197911fb7/packages/adapter-drizzle/src/lib/pg.ts#L398
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    account_type = models.CharField(max_length=255, default="oauth")
    provider = models.CharField(max_length=255)
    provider_account_id = models.CharField(max_length=255)
    refresh_token = models.TextField(max_length=255, default="")
    access_token = models.TextField(max_length=255, default="")
    expires_at = models.DateTimeField(null=True, default=None)
    token_type = models.CharField(max_length=255, default="")
    scope = models.TextField(default="")
    id_token = models.TextField(default="")
    session_state = models.TextField(default="")


class UserProfile(BaseUUID, BaseAutoDate):
    """
    Model for storing user profiles.
    """

    GENDER_CHOICES = [
        ("male", "male"),
        ("female", "female"),
        ("non-binary", "non-binary"),
        ("other", "other"),
        ("unknown", "unknown"),
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
