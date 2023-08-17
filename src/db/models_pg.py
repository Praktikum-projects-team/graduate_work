from sqlalchemy import DateTime, Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Room(Base):
    __tablename__ = 'room'
    id = Column(UUID(as_uuid=True), primary_key=True)
    film_id = Column(UUID(as_uuid=True))
    creator_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime)
    view_progress = Column(Integer)
    is_paused = Column(Boolean)


class Participant(Base):
    __tablename__ = 'participant'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey('room.id'), primary_key=True)


class Message(Base):
    __tablename__ = 'message'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    datetime = Column(DateTime, primary_key=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey('room.id'))
    message = Column(String)
