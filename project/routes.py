from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from db_api import add_user, add_chat, add_message, get_chats, get_messages
from validators import (validate_user_data, validate_chat_data, validate_get_message_data,
                                validate_user_id_field,
                                validate_post_message_data,
                                )


class AddUser(HTTPEndpoint):
    async def post(self, request):
        validated_data = await validate_user_data(request)
        if isinstance(validated_data, dict):
            return JSONResponse(validated_data, status_code=400)
        data = await add_user(validated_data)
        if data.get('user_id'):
            return JSONResponse(data, status_code=201)
        return JSONResponse(data, status_code=400)


class AddChat(HTTPEndpoint):
    async def post(self, request):
        validated_data = await validate_chat_data(request)
        if isinstance(validated_data, dict):
            return JSONResponse(validated_data, status_code=400)
        data = await add_chat(validated_data[0], validated_data[1])
        if data.get('chat_id'):
            return JSONResponse(data, status_code=201)
        return JSONResponse(data, status_code=400)


class AddMessage(HTTPEndpoint):
    async def post(self, request):
        validated_data = await validate_post_message_data(request)
        if isinstance(validated_data, dict):
            return JSONResponse(validated_data, status_code=400)
        data = await add_message(validated_data[0], validated_data[1], validated_data[2])
        if data.get('message_id'):
            return JSONResponse(data, status_code=201)
        return JSONResponse(data, status_code=400)


class GetChats(HTTPEndpoint):
    async def post(self, request):
        validated_data = await validate_user_id_field(request)
        if isinstance(validated_data, dict):
            return JSONResponse(validated_data, status_code=400)
        data = await get_chats(validated_data)
        if data.get('chats'):
            return JSONResponse(data, status_code=201)
        return JSONResponse(data, status_code=400)


class GetMessages(HTTPEndpoint):
    async def post(self, request):
        validated_data = await validate_get_message_data(request)
        if isinstance(validated_data, dict):
            return JSONResponse(validated_data, status_code=400)
        data = await get_messages(validated_data)
        if data.get('messages'):
            return JSONResponse(data, status_code=201)
        return JSONResponse(data, status_code=400)
