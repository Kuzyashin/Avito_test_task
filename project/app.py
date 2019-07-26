import uvicorn
from starlette.applications import Starlette
from starlette.routing import Router, Route

from db_api import database, check_tables
from routes import AddUser, AddChat, AddMessage, GetChats, GetMessages



app = Starlette(debug=True)


@app.on_event("startup")
async def startup():
    await database.connect()
    await check_tables()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


router = Router([
    Route('/users/add', endpoint=AddUser, methods=['POST']),
    Route('/chats/add', endpoint=AddChat, methods=['POST']),
    Route('/chats/get', endpoint=GetChats, methods=['POST']),
    Route('/messages/add', endpoint=AddMessage, methods=['POST']),
    Route('/messages/get', endpoint=GetMessages, methods=['POST']),
])

app.mount('', router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9000)
