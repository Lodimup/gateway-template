from appaccount.models.accounts import User, UserProfile
from ninja import Field, ModelSchema, Schema
from pydantic import field_validator


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserProfileSchema(ModelSchema):
    class Meta:
        model = UserProfile
        exclude = ["id", "user"]


class MeGetOut(Schema):
    user: UserSchema
    user_profile: UserProfileSchema


class MePatchIn(ModelSchema):
    username: str | None = Field(None, min_length=3, max_length=150)

    class Meta:
        model = UserProfile
        exclude = ["id", "user", "created", "updated"]

    @field_validator("gender", check_fields=False)
    def validate_gender(cls, v):
        allowed_genders = [gender[0] for gender in UserProfile.GENDER_CHOICES]
        if v not in allowed_genders:
            raise ValueError(f"gender must be one of {', '.join(allowed_genders)}")
        return v

    @field_validator("username")
    def validate_username(cls, v):
        if User.objects.filter(username=v).exists():
            raise ValueError("username already exists")
        return v


class MePatchOut(MeGetOut): ...
