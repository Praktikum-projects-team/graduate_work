from typing import Optional
from uuid import UUID

from core.base_model import OrjsonBaseModel


class RoomCreateReq(OrjsonBaseModel):
    film_id: UUID
    participants: list[UUID]


class RoomMessagesReq(OrjsonBaseModel):
    message: str


class RoomIsPausedReq(OrjsonBaseModel):
    is_paused: bool


class RoomViewProgressReq(OrjsonBaseModel):
    view_progress: int


class RoomResp(OrjsonBaseModel):
    msg: str
    room_id: Optional[str]


class RoomInfoResp(OrjsonBaseModel):
    id: str
    created_at: str
    creator_id: str
    film_id: str
    is_paused: bool
    messages: list[dict]
    participants: list[str]
    view_progress: int
