from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, status

from services.auth import AuthApi, get_auth_api
from services.connection_manager import ConnectionManager, get_connection_manager
from services.room import RoomService, get_room_service

router = APIRouter()


@router.websocket('/{room_id}')
async def room_websoket(
    *,
    room_id: str,
    token: str = Query(...),
    websocket: WebSocket,
    auth_api: AuthApi = Depends(get_auth_api),
    connection_manager: ConnectionManager = Depends(get_connection_manager),
    room_service: RoomService = Depends(get_room_service),
):
    """Вебсокет комнаты"""

    await auth_api.check_token(token)
    user_id = auth_api.decode_jwt(token)
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid token')

    room = await room_service.get(room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'Room {room_id} not found')

    await connection_manager.connect(room_id, websocket)
    try:
        async for message in room_service.iter_json(websocket, room, user_id):
            await connection_manager.send_message(room_id, message)
    finally:
        await connection_manager.disconnect(room_id, websocket)
