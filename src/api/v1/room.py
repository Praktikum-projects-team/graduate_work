from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, status
from pydantic import ValidationError

from core import models as core_models
from core.security import decode_jwt
from services.auth import AuthApi, get_auth_api
from services.connection_manager import ConnectionManager, get_connection_manager
from services.room import RoomService, get_room_service

router = APIRouter()


@router.websocket('/{room_id}')
async def room_wesoket(
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
    token_payload = decode_jwt(token)
    if token_payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid token')

    user_id = UUID(token_payload['id'])
    room = await room_service.get(room_id)
    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'Room {room_id} not found')

    await connection_manager.connect(room_id, websocket)
    try:
        async for json_data in websocket.iter_json():
            try:
                message = core_models.parse_message(json_data)
                await room_service.handle_message(room, user_id, message)
                await connection_manager.send_message(room_id, message)
            except (ValueError, ValidationError) as e:
                await connection_manager.send_message(
                    room_id=room_id,
                    message=core_models.Error(message=str(e)),
                )
    finally:
        await connection_manager.disconnect(room_id, websocket)
