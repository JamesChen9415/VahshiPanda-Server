from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from .database import get_chat_db
from . import model
from . import schemas
from typing import List

import asyncio
from pprint import pprint


async def insert_doc(
    db: AsyncIOMotorDatabase,
    col: str,
    data: model.ChatChannelModel,
) -> ObjectId | None:
    """
    Insert a single msg into a document.
    """
    try:
        if col not in await db.list_collection_names():
            await db.create_collection(col)

        mycol = db[col]
        result = await mycol.insert_one(
            data.dict(exclude={"chat_channel_id"}, by_alias=True),
        )
        return result.inserted_id
    except Exception as e:
        print(e)
        return None


async def update_one(
    db: AsyncIOMotorDatabase,
    col: str,
    chat_channel_id: str,
    data: model.MessageModel,
) -> ObjectId | None:
    """
    Insert a single msg into a document.
    """
    try:
        if col not in await db.list_collection_names():
            await db.create_collection(col)

        mycol = db[col]

        myquery = {"_id": ObjectId(chat_channel_id)}
        newvalues = {"$push": {"messages": data.dict(by_alias=True)}}
        result = await mycol.update_one(myquery, newvalues)

        if result.modified_count:
            return data.msg_id  # Return the msg_id of the inserted message
        else:
            return None
    except Exception as e:
        print(e)
        return None


async def get_chat_messages(
    db: AsyncIOMotorDatabase,
    col: str,
    chat_channel_id: str,
    skip: int = 0,
    limit: int = 10,
) -> List[dict]:
    """
    Retrieve chat messages from a specific chat channel with paging.

    :param db: The AsyncIOMotorDatabase instance.
    :param col: The collection name.
    :param chat_channel_id: The ID of the chat channel.
    :param skip: Number of messages to skip (for pagination).
    :param limit: Maximum number of messages to return.
    :return: A list of chat messages.
    """
    try:
        mycol = db[col]
        chat_channel = await mycol.find_one({"_id": ObjectId(chat_channel_id)})
        if chat_channel and "messages" in chat_channel:
            # Assuming messages are stored in chronological order
            messages = chat_channel["messages"][skip : skip + limit]
            return messages
        return []
    except Exception as e:
        print(f"Failed to retrieve messages: {e}")
        return []


async def delete_messages(
    db: AsyncIOMotorDatabase, col: str, chat_channel_id: str, message_ids: List[str]
) -> bool:
    """
    Delete specific messages from a chat channel.

    :param db: The AsyncIOMotorDatabase instance.
    :param col: The collection name.
    :param chat_channel_id: The ID of the chat channel.
    :param message_ids: A list of message IDs to be deleted.
    :return: True if the operation was successful, False otherwise.
    """
    try:
        mycol = db[col]
        # Prepare the query to match the chat_channel_id
        myquery = {"_id": ObjectId(chat_channel_id)}
        # Prepare the update command to delete messages with the specified msg_ids
        update_cmd = {"$pull": {"messages": {"msg_id": {"$in": message_ids}}}}
        result = await mycol.update_one(myquery, update_cmd)

        # Check if the update operation was successful
        if result.modified_count > 0:
            print(f"Successfully deleted messages: {message_ids}")
            return True
        else:
            print("No messages were deleted.")
            return False
    except Exception as e:
        print(f"Failed to delete messages: {e}")
        return False


async def count_messages_in_chat_channel(
    db: AsyncIOMotorDatabase, col: str, chat_channel_id: str
) -> int:
    """
    Count the number of messages in a specific chat channel.

    :param db: The AsyncIOMotorDatabase instance.
    :param col: The collection name.
    :param chat_channel_id: The ID of the chat channel to count messages for.
    :return: The number of messages in the chat channel.
    """
    try:
        mycol = db[col]
        pipeline = [
            {"$match": {"_id": ObjectId(chat_channel_id)}},
            {"$project": {"count": {"$size": "$messages"}}},
        ]
        async for result in mycol.aggregate(pipeline):
            return result.get("count", 0)
    except Exception as e:
        print(f"Error counting messages: {e}")
        return 0


async def edit_message(
    db: AsyncIOMotorDatabase,
    col: str,
    chat_channel_id: str,
    msg_id: str,
    new_content: str,
) -> bool:
    mycol = db[col]
    result = await mycol.update_one(
        {"_id": ObjectId(chat_channel_id), "messages.msg_id": msg_id},
        {"$set": {"messages.$.content": new_content}},
    )
    return result.modified_count > 0


async def search_messages(
    db: AsyncIOMotorDatabase,
    col: str,
    chat_channel_id: str,
    search_text: str,
) -> List[dict]:
    mycol = db[col]
    query = {
        "_id": ObjectId(chat_channel_id),
        "messages.content": {"$regex": search_text, "$options": "i"},
    }
    projection = {
        "messages": {
            "$elemMatch": {
                "content": {"$regex": search_text, "$options": "i"},
            }
        }
    }
    chat_channel = await mycol.find_one(query, projection)
    if chat_channel and "messages" in chat_channel:
        return chat_channel["messages"]
    return []


async def add_member_to_channel(
    db: AsyncIOMotorDatabase,
    col: str,
    chat_channel_id: str,
    member_id: str,
) -> bool:
    """
    Adds a user to the specified chat channel.

    :param db: The AsyncIOMotorDatabase instance.
    :param col: The collection name.
    :param chat_channel_id: The ID of the chat channel.
    :param member_id: The ID of the user to add to the channel.
    :return: True if the operation was successful, False otherwise.
    """
    try:
        mycol = db[col]
        result = await mycol.update_one(
            {"_id": ObjectId(chat_channel_id)},
            {
                "$addToSet": {"members": member_id},
            },
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Failed to add user to channel: {e}")
        return False


async def remove_member_from_channel(
    db: AsyncIOMotorDatabase,
    col: str,
    chat_channel_id: str,
    member_id: str,
) -> bool:
    """
    Removes a user from the specified chat channel.

    :param db: The AsyncIOMotorDatabase instance.
    :param col: The collection name.
    :param chat_channel_id: The ID of the chat channel.
    :param member_id: The ID of the user to remove from the channel.
    :return: True if the operation was successful, False otherwise.
    """
    try:
        mycol = db[col]
        result = await mycol.update_one(
            {"_id": ObjectId(chat_channel_id)},
            {
                "$pull": {"members": member_id},
            },
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Failed to remove user from channel: {e}")
        return False


# ==== insert =======
# # prepare chat msg
# msg = {
#     "msg_from": "James",
#     "msg_to": "Group",
#     "content": "This is a test message",
# }
# msg = model.MessageModel(**msg)

# # prepare chat channel
# chat = {
#     "members": ["James", "Mehdi"],
#     "messages": [msg.dict(by_alias=True)],
# }
# # chat = {
# #     "members": ["James", "Mehdi"],
# #     "messages": [],
# # }
# chat_channel = model.ChatChannelModel(**chat)

# # # get collection in db
# collection = "col1"
# chat_db = get_chat_db()
# result = asyncio.run(
#     insert_doc(
#         chat_db,
#         collection,
#         chat_channel,
#     )
# )
# print(result)

# ==== update =======
# msg = {
#     "chat_channel_id": "65f53b1bb1bb952dca49a62b",
#     "msg_from": "James",
#     "msg_to": "James",
#     "content": "This is a test message from James",
# }


# chat_channel_id = msg["chat_channel_id"]
# del msg["chat_channel_id"]

# msg = model.MessageModel(**msg)

# collection = "col1"
# chat_db = get_chat_db()
# result = asyncio.run(
#     update_one(
#         chat_db,
#         collection,
#         chat_channel_id,
#         msg,
#     )
# )
# print(result)

# ======= retrieve =======
# chat_channel_id = "65f460030eff0d3fd061e554"
# skip = 1
# limit = 3

# collection = "col1"
# chat_db = get_chat_db()
# result = asyncio.run(
#     get_chat_messages(
#         chat_db,
#         collection,
#         chat_channel_id,
#         skip,
#         limit,
#     )
# )
# pprint(result)


# ======= delete =======
# chat_channel_id = "65f518d025d4f640ad029505"
# skip = 1
# limit = 3
# message_ids_to_delete = [
#     "05324f12eaf042f78ff41115518a30a1",
#     "418a25bae31d4a8ebf4056384da5dcc7",
# ]
# collection = "col1"
# chat_db = get_chat_db()
# success = asyncio.run(
#     delete_messages(
#         chat_db,
#         collection,
#         chat_channel_id,
#         message_ids_to_delete,
#     )
# )

# if success:
#     print("Messages deleted successfully.")
# else:
#     print("Failed to delete messages.")


# pprint(success)


# ===== count messages ======
# chat_channel_id = "65f518d025d4f640ad029505"
# collection = "col1"
# chat_db = get_chat_db()
# message_count = asyncio.run(
#     count_messages_in_chat_channel(
#         chat_db,
#         collection,
#         chat_channel_id,
#     )
# )

# pprint(message_count)

# # ===== add members to channel ======

# member_id = "Yaya"
# chat_channel_id = "65f518d025d4f640ad029505"
# collection = "col1"
# chat_db = get_chat_db()
# success = asyncio.run(
#     add_member_to_channel(
#         chat_db,
#         collection,
#         chat_channel_id,
#         member_id,
#     )
# )

# pprint(success)

# ===== remove members to channel ======

# member_id = "Yaya"
# chat_channel_id = "65f518d025d4f640ad029505"
# collection = "col1"
# chat_db = get_chat_db()
# success = asyncio.run(
#     remove_member_from_channel(
#         chat_db,
#         collection,
#         chat_channel_id,
#         member_id,
#     )
# )

# pprint(success)
