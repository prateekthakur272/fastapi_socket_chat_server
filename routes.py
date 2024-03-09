from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates('templates')

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections:list[WebSocket] = []
        
    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    async def disconnect(self, websocket:WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message_personal(self, websocket:WebSocket, message:str):
        await websocket.send_text(message)
        
    async def send_message_broadcast(self, message:str):
        for client in self.active_connections:
            await client.send_text(message)

@router.get('/')
def chat(request:Request):
    return templates.TemplateResponse('chat.html', {'request':request})

manager = ConnectionManager()
@router.websocket('/chat/{client_id}')
async def chat_socket(websocket:WebSocket, client_id:int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message_broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
