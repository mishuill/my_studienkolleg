from pydantic import BaseModel, Field, EmailStr
from pydantic_mongo import PydanticObjectId
from ..config import AccessLevel

# fmt: off

# TODO: rework to use fields as variables (with Annotated[])
username_field = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Username must be 3-20 characters long and can only contain letters, numbers, underscores, periods, and hyphens"
    )


class DBUser(BaseModel):
    """
    Base User Data Model
    """

    id: PydanticObjectId | None = Field(
        None,
        alias="_id",
        description="Entry ID in MongoDB Collection. Also User's UUID"
        )
    username: str = username_field
    hashed_password: str = Field(
        ..., 
        description="Hashed user password"
    )
    email: EmailStr | None = Field(
        None,
        description="A valid email address"
    )
    access_level: AccessLevel = Field(
        AccessLevel.default,
        description="User's access level"
    )
    user_metadata: dict | None = Field(
        None,
        description="User's metadata"
    )
    
    class Config:
        from_attributes = True
        json_encoders = {
            PydanticObjectId: str
        }
# fmt: on
