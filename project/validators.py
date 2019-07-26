import json
from html import escape

from db_api import check_user_exists, check_chat_exists


async def validate_user_data(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return {
            'error': 'No data provided'
        }
    username = data.get('username')
    if not username:
        return {
            "error": "'username' field required"
        }
    return escape(username)


async def validate_chat_data(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return {
            'error': 'No data provided'
        }
    name = data.get('name')
    if not name:
        return {
            "error": "'name' field required"
        }
    users = data.get('users')
    if not users:
        return {
            "error": "'users' field required"
        }
    if not isinstance(users, list):
        return {
            "Detail": "'users' must be list instance"
        }
    for user in users:
        try:
            int(user)
        except ValueError:
            return {
                "error": "'user' must be integer"
            }
        exists = await check_user_exists(user)
        if not exists:
            return {
                "error": "'user_id = {}' does not exists".format(user)
            }
    return [escape(name), users]


async def validate_post_message_data(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return {
            'error': 'No data provided'
        }
    chat_id = data.get('chat')
    if not chat_id:
        return {
            "error": "'chat' field required"
        }
    try:
        int(chat_id)
    except ValueError:
        return {
            "error": "'chat' must be integer"
        }
    exists = await check_chat_exists(chat_id)
    if not exists:
        return {
            "error": "'chat = {}' does not exists".format(chat_id)
        }
    user_id = data.get('author')
    if not user_id:
        return {
            "error": "'author' field required"
        }
    try:
        int(user_id)
    except ValueError:
        return {
            "error": "'author' must be integer"
        }
    exists = await check_user_exists(user_id)
    if not exists:
        return {
            "error": "'author = {}' does not exists".format(user_id)
        }
    text = data.get('text')
    if not text:
        return {
            "error": "'text' field required"
        }
    return [chat_id, user_id, escape(text)]


async def validate_get_message_data(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return {
            'error': 'No data provided'
        }
    chat_id = data.get('chat')
    if not chat_id:
        return {
            "error": "'chat' field required"
        }
    try:
        int(chat_id)
    except ValueError:
        return {
            "error": "'chat' must be integer"
        }
    exists = await check_chat_exists(chat_id)
    if not exists:
        return {
            "error": "'chat = {}' does not exists".format(chat_id)
        }
    return chat_id


async def validate_user_id_field(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return {
            'error': 'No data provided'
        }
    user_id = data.get('user_id')
    if not user_id:
        return {
            "error": "'user_id' field required"
        }
    try:
        int(user_id)
    except ValueError:
        return {
            "error": "'user_id' must be integer"
        }
    exists = await check_user_exists(user_id)
    if not exists:
        return {
            "error": "'user_id = {}' does not exists".format(user_id)
        }
    return user_id


async def validate_chat_id_field(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        return {
            'error': 'No data provided'
        }
    chat_id = data.get('chat')
    if not chat_id:
        return {
            "error": "'chat' field required"
        }
    try:
        int(chat_id)
    except ValueError:
        return {
            "error": "'chat' must be integer"
        }
    exists = await check_chat_exists(chat_id)
    if not exists:
        return {
            "error": "'chat = {}' does not exists".format(chat_id)
        }
    return chat_id
