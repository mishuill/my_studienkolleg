from pydantic import BaseModel, Field, EmailStr
from pydantic_mongo import PydanticObjectId

from ..config import AccessLevel


class RegisterUser(BaseModel):
    """
    User registration schema
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Username must be 3-20 characters long and can only contain letters, numbers, underscores, periods, and hyphens",
    )
    password: str = Field(
        ...,
        pattern=r"^[A-Za-z0-9@$!%*#?&]+$",
        min_length=6,
        max_length=128,
        description="Password must be 6-128 characters long and can only contain letters, numbers, and symbols (@$!%*#?&)",
    )
    email: EmailStr | None = Field(None, description="A valid email address")

    class Config:
        from_attributes = True


# TODO: Make a login validator, so there's at least email or username provided (now only username is required)
class LoginUser(RegisterUser):
    """
    User login schema
    """

    pass


class UpdateUser(BaseModel):
    """
    User info update schema
    """

    id: str = Field(
        ...,
        description="The ID of user to be updated",
    )
    username: str | None = Field(
        None,
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Username must be 3-20 characters long and can only contain letters, numbers, underscores, periods, and hyphens",
    )
    password: str | None = Field(
        None,
        pattern=r"^[A-Za-z0-9@$!%*#?&]+$",
        min_length=6,
        max_length=128,
        description="Password must be 6-128 characters long and can only contain letters, numbers, and symbols (@$!%*#?&)",
    )
    email: EmailStr | None = Field(None, description="A valid email address")
    user_metadata: dict | None = Field(None, description="User's metadata")

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    User registration return schema
    """

    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True


class UserInfoResponse(BaseModel):
    """
    User information return schema
    """

    id: PydanticObjectId
    username: str
    email: EmailStr | None
    access_level: AccessLevel
    user_metadata: dict | None

    class Config:
        from_attributes = True
