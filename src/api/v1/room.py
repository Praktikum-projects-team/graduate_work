import logging

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, status

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.room import RoomReq, RoomResp
from services.auth import AuthApi, get_auth_api
from services.connection_manager import ConnectionManager, get_connection_manager
from services.room import RoomService, get_room_service

router = APIRouter()
auth_api = AuthApi()


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


@router.post(
    '/',
    response_model=RoomResp,
    description='Создание комнаты',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_room(
        data: RoomReq,
        token: str = Depends(BaseJWTBearer()),
        room_service: RoomService = Depends(get_room_service)
) -> RoomResp:
    # user_info = jwt_bearer.decode_jwt(token)
    try:
        # await room_service.create(user_id=user_info['id'], film_id=data.film_id)
        await room_service.create(token=token, film_id=data.film_id)
    except Exception as e:
        logging.error(e)
        return RoomResp(msg='Creating room is failed')

    return RoomResp(msg='Room created')
