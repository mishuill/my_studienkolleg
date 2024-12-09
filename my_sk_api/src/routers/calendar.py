from fastapi import APIRouter, Body, Query, Depends

from ..domain.calendar.models import DBEvent, DBUpdateEvent
from ..domain.calendar.schemas import *

from ..domain.calendar.service import *
from ..dependencies import JWTBearer, get_user_id

calendar_router = APIRouter(tags=["calendar"])


@calendar_router.get(f"/calendar/", dependencies=[Depends(JWTBearer())])
async def get_event_endpoint(event: GetEvent = Query(...), user_id=Depends(get_user_id)) -> GetEventResponse:
    document_id = event.id

    document = await get_event(id=document_id, user_id=user_id)
    if document:
        return {"document": document}

@calendar_router.post(f"/calendar/", dependencies=[Depends(JWTBearer())])
async def create_event_endpoint(event: CreateEvent = Body(...), user_id: str = Depends(get_user_id)) -> CreateEventResponse:
    event = event.model_dump()
    event["user_id"] = user_id

    event_entry = DBEvent(**event)
    document = await insert_event(event=event_entry)
    return {"id": str(document.id)}

@calendar_router.patch(f"/calendar/", dependencies=[Depends(JWTBearer())])
async def update_event_endpoint(event: UpdateEvent = Query(...), user_id: str = Depends(get_user_id)) -> bool:
    event = event.model_dump()

    event["user_id"] = user_id
    event["_id"] = event.pop("id")

    event_entry = DBUpdateEvent(**event)
    try:
        await update_event(event_entry)
        return True
    except Exception as e:
        print(e)
        return False

@calendar_router.delete(f"/calendar/", dependencies=[Depends(JWTBearer())])
async def update_event_endpoint(event: DeleteEvent = Query(...), user_id: str = Depends(get_user_id)) -> bool:
    try:
        await delete_event(id=event.id, user_id=user_id)
        return True
    except Exception as e:
        print(e)
        return False

@calendar_router.get(f"/calendar/list", dependencies=[Depends(JWTBearer())])
async def list_events_endpoint(query_params: ListEvents = Query(...), user_id: str = Depends(get_user_id)) -> ListEventsResponse:
    documents = await list_events_of_user(limit=query_params.limit, tags=query_params.tags, user_id=user_id)
    if documents:
        return {"documents": documents, "number_of_documents": len(documents)}
    else:
        return {"documents": [], "number_of_documents": 0}
