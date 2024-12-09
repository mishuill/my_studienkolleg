from passlib.context import CryptContext

from .models import DBUser
from ...database import (
    find_document,
    get_document,
    insert_document,
    update_document,
    replace_document,
    delete_document,
    list_docuemnts,
    db,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_collection = db.get_collection("users")


async def find_user(filter) -> DBUser | None:
    result = await find_document(collection=users_collection, filter=filter)
    if result:
        return DBUser.model_validate(result)
    else:
        return None


async def get_user(id: str) -> DBUser | None:
    result = await get_document(collection=users_collection, id=id)
    if result:
        return DBUser.model_validate(result)
    else:
        return None


async def insert_user(user: DBUser) -> DBUser | None:
    result = await insert_document(collection=users_collection, document=user)
    if result:
        return DBUser.model_validate(result)
    else:
        return None


async def update_user(id: str, user: DBUser) -> DBUser | None:
    result = await update_document(collection=users_collection, id=id, document=user)
    if result:
        return DBUser.model_validate(result)
    else:
        return None


async def replace_user(id: str, user: DBUser) -> DBUser | None:
    result = await replace_document(collection=users_collection, id=id, document=user)
    if result:
        return DBUser.model_validate(result)
    else:
        return None


async def delete_user(id: str) -> DBUser | None:
    result = await delete_document(collection=users_collection, id=id)
    if result:
        return DBUser.model_validate(result)
    else:
        return None


async def list_users() -> list[DBUser]:
    results = await list_docuemnts(collection=users_collection)
    if results:
        results = [DBUser.model_validate(result) for result in results]
        return results
    else:
        return None
    

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
