from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId
from datetime import datetime


class DBEvent(BaseModel):
    """
    Base User Data Model
    """

    id: PydanticObjectId | None = Field(
        None, alias="_id", description="Entry ID in MongoDB Collection."
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.\s-]+$",
        description="A valid event name",
    )
    user_id: str = Field(
        ...,
        description="The ID of user, that created the event"
    )
    start: datetime = Field(
        ...,
        description="A valid start date of the event. Should contain the day, as well, as the time",
    )
    end: datetime = Field(
        ...,
        description="A valid end date of the event. Should contain the day, as well, as the time",
    )
    description: str | None = Field(
        None,
        description="The events description")
    tags: list[str] | None = Field(
        None, 
        description="A set of tags associated with the event"
    )

    # TODO: convert to field serializers
    class Config:
        from_attributes = True
        json_encoders = {
            PydanticObjectId: str,
        }

class DBUpdateEvent(BaseModel):
    """
    Base User Data Model
    """

    id: str = Field(
        ..., 
        alias="_id",
        description="Entry ID in MongoDB Collection."
    )
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.\s-]+$",
        description="A valid event name",
    )
    user_id: str | None = Field(
        default=None, 
        description="The ID of user, that created the event"
    )
    start: datetime | None= Field(
        default=None,
        description="A valid start date of the event. Should contain the day, as well, as the time",
    )
    end: datetime | None= Field(
        default=None,
        description="A valid end date of the event. Should contain the day, as well, as the time",
    )