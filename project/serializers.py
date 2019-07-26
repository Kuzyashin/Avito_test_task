def serialize_chats(raw_data):
    chats = []
    for chat in raw_data:
        chats.append({
            "chat_id": chat[0],
            "name": chat[1],
            "created_at": chat[2]
        })
    return {"chats": chats}


def serialize_messages(raw_data):
    messages = []
    for message in raw_data:
        messages.append({
            "message_id": message[0],
            "chat": message[1],
            "author": message[2],
            "text": message[3],
            "created_at": message[4]
        })
    return {"messages": messages}
