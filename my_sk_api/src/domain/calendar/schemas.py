from pydantic import BaseModel, Field
from datetime import datetime

from .models import DBEvent

def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

class CreateEvent(BaseModel):
    """
    Event creation (schema)
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.\s-]+$",
        description="A valid event name",
    )
    start: datetime = Field(
        ...,
        description="A valid start date of the event. Should contain the day, as well, as the time",
    )
    end: datetime = Field(
        ...,
        description="A valid end date of the event. Should contain the day, as well, as the time",
    )
    description: str | None = Field(None, description="The events description")
    tags: list[str] | None = Field(
        None, description="A list of tags associated with the event"
    )

    class Config:
        from_attributes = True
        json_encodes = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }


class UpdateEvent(BaseModel):
    """
    Event update (schema)
    """
    id: str = Field(
        ...,
        description="The ID of event to be fetched",
    )
    name: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.\s-]+$",
        description="A valid event name",
    )
    start: datetime | None = Field(
        None,
        strict=True,
        description="A valid start date of the event. Should contain the day, as well, as the time",
    )
    end: datetime | None = Field(
        None,
        strict=True,
        description="A valid end date of the event. Should contain the day, as well, as the time",
    )
    description: str | None = Field(
        None, 
        description="The events description"
    )
    tags: set | None = Field(
        None,
        description="A set of tags associated with the event"
    )

    class Config:
        from_attributes = True


class GetEvent(BaseModel):
    """
    Get event with id (schema)
    """
    id: str = Field(
        ...,
        description="The ID of event to be fetched",
    )

class DeleteEvent(BaseModel):
    """
    Event deletion (schema)
    """
    id: str = Field(
        ...,
        description="The ID of event to be deleted",
    )


class ListEvents(BaseModel):
    """
    List all events of user (schema)
    """
    limit: int = Field(
        50, 
        gt=0, 
        le=500, 
        description="Max number of events to be returned"
    )
    tags: list[str] | None = Field(
        None, 
        min_length=1,
        description="The tags used to search for events"
    )
    


class CreateEventResponse(BaseModel):
    """
    Create document (response schema)
    """

    id: str = Field(..., description="Id of created document")


class GetEventResponse(BaseModel):
    """
    Fetched document (response schema)
    """

    document: DBEvent = Field(..., description="Fetched document")


class ListEventsResponse(BaseModel):
    """
    List all events of user (response schema)
    """

    documents: list[DBEvent | None]= Field(
        [],
        description="List of found events",
    )
    number_of_documents: int = Field(
        0, 
        ge=0,
        description="The number of found events"
    )
