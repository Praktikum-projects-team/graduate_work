from uuid import UUID

from core.base_model import OrjsonBaseModel


class RoomReq(OrjsonBaseModel):
    film_id: UUID
    participants: list[UUID]


class RoomResp(OrjsonBaseModel):
    msg: str


class RoomInfoResp(OrjsonBaseModel):
    id: str
    created_at: str
    creator_id: str
    film_id: str
    is_paused: bool
    messages: list[str]
    participants: list[str]
    view_progress: int
