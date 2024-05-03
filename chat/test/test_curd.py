"""
Unit Test needs to be completed
"""

# # test_chat_operations.py
# import pytest
# from bson import ObjectId
# from unittest.mock import AsyncMock, MagicMock

# # Import your functions here. This assumes they're accessible via 'from chat_operations import ...'
# from app.mongodb_app.crud import (
#     insert_doc,
#     update_one,
#     get_chat_messages,
#     delete_messages,
#     count_messages_in_chat_channel,
#     edit_message,
#     search_messages,
#     add_member_to_channel,
#     remove_member_from_channel,
# )


# @pytest.mark.asyncio
# async def test_insert_doc(mocker):
#     db = mocker.MagicMock()
#     col = "test_col"
#     data = MagicMock()  # Mock your ChatChannelModel
#     data.dict.return_value = {"members": [], "messages": []}
#     db[col].insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))

#     result = await insert_doc(db, col, data)
#     assert result is not None
#     db[col].insert_one.assert_awaited_once()


# @pytest.mark.asyncio
# async def test_update_one(mocker):
#     db = mocker.MagicMock()
#     col = "test_col"
#     chat_channel_id = str(ObjectId())
#     data = MagicMock()  # Mock your MessageModel
#     data.dict.return_value = {"msg_id": "some_id", "content": "new message"}
#     db[col].update_one = AsyncMock(return_value=MagicMock(modified_count=1))

#     result = await update_one(db, col, chat_channel_id, data)
#     assert result is not None
#     db[col].update_one.assert_awaited_once()


# @pytest.mark.asyncio
# async def test_count_messages_in_chat_channel(mocker):
#     db = mocker.MagicMock()
#     col = "test_col"
#     chat_channel_id = str(ObjectId())
#     mock_aggregate = AsyncMock()
#     mock_aggregate.__aiter__.return_value = iter([{"count": 5}])
#     db[col].aggregate = mock_aggregate

#     count = await count_messages_in_chat_channel(db, col, chat_channel_id)
#     assert count == 5


# @pytest.mark.asyncio
# async def test_add_member_to_channel(mocker):
#     db = mocker.MagicMock()
#     col = "test_col"
#     chat_channel_id = str(ObjectId())
#     member_id = "member123"
#     db[col].update_one = AsyncMock(return_value=MagicMock(modified_count=1))

#     success = await add_member_to_channel(db, col, chat_channel_id, member_id)
#     assert success is True


# @pytest.mark.asyncio
# async def test_remove_member_from_channel(mocker):
#     db = mocker.MagicMock()
#     col = "test_col"
#     chat_channel_id = str(ObjectId())
#     member_id = "member123"
#     db[col].update_one = AsyncMock(return_value=MagicMock(modified_count=1))

#     success = await remove_member_from_channel(db, col, chat_channel_id, member_id)
#     assert success is True
