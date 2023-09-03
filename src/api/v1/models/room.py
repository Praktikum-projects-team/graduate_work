from uuid import UUID

from core.base_model import OrjsonBaseModel


class RoomReq(OrjsonBaseModel):
    film_id: UUID
    participants: list[UUID]


class RoomResp(OrjsonBaseModel):
    msg: str
