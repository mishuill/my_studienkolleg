from bson import ObjectId

from .models import DBEvent, DBUpdateEvent
from ...database import (
    find_document,
    get_document,
    insert_document,
    update_document,
    replace_document,
    delete_document,
    list_docuemnts,
    find_docuemnts,
    db,
)

events_collection = db.get_collection("events")


async def find_event(filter) -> DBEvent | None:
    result = await find_document(collection=events_collection, filter=filter)
    if result:
        return DBEvent.model_validate(result)
    else:
        return None


async def get_event(id: str, user_id: str) -> DBEvent | None:
    return await find_document(
        collection=events_collection, filter={"_id": ObjectId(id), "user_id": user_id}
    )


async def insert_event(event: DBEvent) -> DBEvent | None:
    result = await insert_document(collection=events_collection, document=event)
    if result:
        return DBEvent.model_validate(result)
    else:
        return None


async def update_event(event: DBUpdateEvent) -> DBEvent | None:
    result = await update_document(collection=events_collection, document=event)
    if result:
        return DBEvent.model_validate(result)
    else:
        return None


async def replace_event(id: str, event: DBEvent) -> DBEvent | None:
    result = await replace_document(collection=events_collection, id=id, document=event)
    if result:
        return DBEvent.model_validate(result)
    else:
        return None


async def delete_event(id: str, user_id: str) -> DBEvent | None:
    event = await get_event(id=id, user_id=user_id)
    if event:
        result = await delete_document(collection=events_collection, id=id)
        if result:
            return DBEvent.model_validate(result)
        else:
            return None
    else:
        raise Exception("File does not belong to the user")


async def list_events_of_user(limit: int, user_id: str) -> list[DBEvent] | None:
    results = await find_docuemnts(
        collection=events_collection, 
        filter={"user_id": user_id},
        limit=limit
    )
    if results:
        results = [DBEvent.model_validate(result) for result in results]
        return results
    else:
        return None


async def list_events_of_user_by_tag(user_id: str, tag: str) -> list[DBEvent] | None:
    return await list_events_of_user(user_id=user_id, tags=[tag])


async def list_events_of_user(user_id: str, limit: int | None = None, tags: list[str] | None = None) -> list[DBEvent] | None:
    filter = {"user_id": user_id}
    if tags:
        filter["tags"] = {"$in": tags}
    
    results = await find_docuemnts(collection=events_collection, filter=filter, limit=limit)
    if results:
        results = [DBEvent.model_validate(result) for result in results]
        return results
    else:
        return None
