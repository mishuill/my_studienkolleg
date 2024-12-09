import os
import asyncio

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from bson import ObjectId
from pydantic import BaseModel
from pymongo.errors import ServerSelectionTimeoutError

SERVER_TIMEOUT_MS = os.environ["SERVER_TIMEOUT_MS"]

async def ping_server(client: AsyncIOMotorClient):
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except ServerSelectionTimeoutError as e:
        raise Exception(f"Seems like your MongoDB server is down: {e}")


def setup_db(url: str, db_name: str) -> AsyncIOMotorDatabase:
    mongo_client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=SERVER_TIMEOUT_MS)
    loop = asyncio.get_event_loop()
    loop.create_task(ping_server(mongo_client))
    db = getattr(mongo_client, db_name)
    return db


db = setup_db(os.environ["MONGODB_URL"], os.environ["DB_NAME"])


async def find_document(collection: AsyncIOMotorCollection, filter: dict) -> object:
    """
    Find a document in a collection and return it.
    If no document was found, the function returns <None>
    """

    found_document = await collection.find_one(filter)
    return found_document


async def find_docuemnts(collection: AsyncIOMotorCollection, filter: dict, limit: int | None = None) -> object:
    """
    List all documents in a collection.
    If no documents was found, the function returns <None>
    """
    if limit:
        cursor = collection.find(filter).limit(limit)
    else:
        cursor = collection.find(filter)
    found_documents = list(await cursor.to_list())
    return found_documents

async def list_docuemnts(collection: AsyncIOMotorCollection) -> BaseModel:
    """
    List all documents in a collection.
    If no documents was found, the function returns <None>
    """

    found_documents = list(await collection.find().to_list())
    return found_documents

async def get_document(collection: AsyncIOMotorCollection, id: str) -> BaseModel:
    """
    Find a document by ID and return it.
    If no docuemnt was found, the function returns <None>
    """
    found_document = await find_document(collection, {"_id": ObjectId(id)})
    return found_document


async def insert_document(collection: AsyncIOMotorCollection, document: BaseModel) -> BaseModel:
    """
    Create a new document.
    If creation was not successful, the function returns <None>
    """

    result = await collection.insert_one(
        document.model_dump(by_alias=True, exclude=["id"])
    )
    inserted_document = await get_document(
        collection, ObjectId(result.inserted_id)
    )
    return inserted_document


async def update_document(collection: AsyncIOMotorCollection, document: BaseModel) -> BaseModel:
    """
    Update a document.
    If no document was found, the function returns <None>
    """

    updated_document = await collection.find_one_and_update(
        {"_id": ObjectId(document.id)},
        {"$set": document.model_dump(by_alias=True, exclude=["id"], exclude_defaults=True)},
    )
    return updated_document


async def replace_document(collection: AsyncIOMotorCollection, id: str, document: BaseModel) -> BaseModel:
    """
    Find and replace a document.
    If replacment was not successful, the function returns <None>
    """

    replaced_document = await collection.find_one_and_replace(
        {"id": id}, {"$set": document.model_dump(by_alias=True, exclude=["id"])}
    )
    return replaced_document


async def delete_document(collection: AsyncIOMotorCollection, id: str) -> bool:
    """
    Delete a document.
    If deletion was not successful, the function returns <None>
    """

    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    print(delete_result.deleted_count)
    return True if delete_result.deleted_count > 0 else False


