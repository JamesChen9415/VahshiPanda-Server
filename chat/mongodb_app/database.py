import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi


def get_chat_db() -> AsyncIOMotorDatabase:
    # get the host and port numbers from the environment variables
    MONGODBDB_HOST = os.environ.get("MONGODBDB_HOST", "localhost")
    MONGODBDB_PORT = os.environ.get("MONGODBDB_PORT", "27017")
    MONGODBDB_USER = os.environ.get("MONGODBDB_USER", "user")
    MONGODBDB_PASSWORD = os.environ.get("MONGODBDB_PASSWORD", "password")
    uri = f"mongodb://{MONGODBDB_USER}:{MONGODBDB_PASSWORD}@{MONGODBDB_HOST}:{MONGODBDB_PORT}"
    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
    chat_db = client.get_database("chat_db")
    return chat_db
