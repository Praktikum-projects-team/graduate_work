import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, status, Request
from starlette.responses import JSONResponse

from api.v1.auth.auth_bearer import BaseJWTBearer
from api.v1.models.room import RoomInfoResp, RoomReq, RoomResp
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
        request: Request,
        token: str = Depends(BaseJWTBearer()),
        room_service: RoomService = Depends(get_room_service)
) -> RoomResp:
    print('start room creation')
    user = request.token_payload
    room = await room_service.create(user, film_id=data.film_id, participants=data.participants, token=token)

    return RoomResp(msg='Room created', room_id=str(room.id))


@router.get(
    '/{room_id}',
    response_model=RoomInfoResp,
    description='Получение информации о комнате',
    dependencies=[Depends(BaseJWTBearer())]
)
async def get_room_info(
        room_id: str,
        room_service: RoomService = Depends(get_room_service)
) -> JSONResponse | RoomResp | RoomInfoResp:
    room_info = await room_service.get(room_id=room_id)
    if not room_info:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={'msg': 'Room not found'})

    return RoomInfoResp(
        id=str(room_info.id),
        created_at=str(room_info.created_at),
        creator_id=str(room_info.creator_id),
        film_id=str(room_info.film_id),
        is_paused=room_info.is_paused,
        messages=room_info.messages,
        participants=[str(participant) for participant in room_info.participants],
        view_progress=room_info.view_progress
    )
