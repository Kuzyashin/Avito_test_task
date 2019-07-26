import sqlite3
from datetime import datetime

import databases
from starlette.config import Config

from serializers import serialize_chats, serialize_messages

config = Config('.env')
DATABASE_URL = config('DATABASE_URL')
database = databases.Database(DATABASE_URL)


async def create_users_table():
    query = """CREATE TABLE Users (
                  id INTEGER PRIMARY KEY, 
                  username VARCHAR(30) UNIQUE, 
                  created_at TEXT
            )"""
    await database.execute(query=query)


async def create_chats_table():
    query = """CREATE TABLE Chats (
                  id INTEGER PRIMARY KEY, 
                  name VARCHAR(50) UNIQUE, 
                  created_at TEXT
            )"""
    await database.execute(query=query)


async def create_chat_users_table():
    query = """CREATE TABLE ChatUsers (
                  id INTEGER PRIMARY KEY, 
                  user_id INTEGER,
                  chat_id INTEGER,
                  FOREIGN KEY (user_id) REFERENCES Users (id),
                  FOREIGN KEY (chat_id) REFERENCES Chats (id),
                  UNIQUE (user_id, chat_id)
            )"""
    await database.execute(query=query)


async def create_messages_table():
    query = """CREATE TABLE Messages (
                  id INTEGER PRIMARY KEY, 
                  chat INTEGER, 
                  author INTEGER,
                  text TEXT,
                  created_at TEXT,
                  FOREIGN KEY (chat) REFERENCES Chats (id),
                  FOREIGN KEY (author) REFERENCES Users (id)
            )"""
    await database.execute(query=query)


async def check_tables():
    await database.execute("PRAGMA foreign_keys = ON;")
    tables = ['users', 'chats', 'chat_users', 'messages']
    for table in tables:
        try:
            await eval(f'create_{table}_table()')
        except sqlite3.OperationalError:
            pass


async def add_user(username):
    query = """INSERT INTO Users(username, created_at) VALUES (:username, :created_at)"""
    values = {"username": username, "created_at": datetime.now()}
    try:
        user_id = await database.execute(query=query, values=values)
        return {"user_id": user_id}
    except sqlite3.IntegrityError as e:
        return {'error': e.args}


async def create_m2m_chat_users(chat_id, user_id):
    query = """INSERT INTO ChatUsers(chat_id, user_id) VALUES (:chat_id, :user_id)"""
    values = {"chat_id": chat_id, "user_id": user_id}
    await database.execute(query=query, values=values)


async def add_chat(name, users):
    query = """INSERT INTO Chats(name, created_at) VALUES (:name, :created_at)"""
    values = {"name": name, "created_at": datetime.now()}
    try:
        data = await database.execute(query=query, values=values)
    except sqlite3.IntegrityError as e:
        return {'error': e.args}
    for user in users:
        try:
            await create_m2m_chat_users(data, user)
        except sqlite3.IntegrityError:
            pass
    return {'chat_id': data}


async def add_message(chat_id, user_id, text):
    query = """INSERT INTO "Messages"(author, chat, text, created_at) VALUES (:user_id, :chat_id, :text, :created_at)"""
    values = {"user_id": user_id, "chat_id": chat_id, "text": text, "created_at": datetime.now()}
    data = await database.execute(query=query, values=values)
    return {'message_id': data}


async def get_chats(user_id):
    query = """SELECT chat_id, name, created_at FROM ChatUsers 
               JOIN Chats ON Chats.id = ChatUsers.chat_id
               LEFT JOIN 
               (SELECT chat, max(created_at) AS last_msg_created FROM Messages GROUP BY chat) 
               last_msg ON last_msg.chat = Chats.id
               WHERE user_id = :user_id
               ORDER BY last_msg_created DESC
            """
    values = {"user_id": user_id}
    data = await database.fetch_all(query=query, values=values)
    response = serialize_chats(data)
    return response


async def get_messages(chat_id):
    query = """SELECT * FROM Messages WHERE chat = :chat_id ORDER BY created_at DESC"""
    values = {"chat_id": chat_id}
    data = await database.fetch_all(query=query, values=values)
    response = serialize_messages(data)
    return response


async def check_user_exists(user_id):
    query = """SELECT id FROM "Users" WHERE id = :user_id"""
    values = {"user_id": user_id}
    data = await database.fetch_all(query=query, values=values)
    if len(data):
        return True


async def check_chat_exists(chat_id):
    query = """SELECT id FROM "Chats" WHERE id = :chat_id"""
    values = {"chat_id": chat_id}
    data = await database.fetch_all(query=query, values=values)
    if len(data):
        return True
