from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Text
import datetime
from sqlalchemy.orm import relationship

from backend.app.config.db import Base


class SessionModel(Base):
    __tablename__ ="session"

    id=Column(Integer,primary_key=True)
    user_name=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=datetime.datetime.now)

    messages=relationship("MessageModel",back_populates="session",cascade="all, delete-orphan")

class MessageModel(Base):
    __tablename__ ="message"

    id=Column(Integer,primary_key=True)
    session_id =Column(Integer,ForeignKey("session.id"),nullable=False)
    sender_type=Column(String(50),nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.datetime.now)

    session = relationship("SessionModel", back_populates="messages")
    logs=relationship("LogModel",back_populates="message",cascade="all, delete-orphan")

class LogModel(Base):
    __tablename__ ="log"

    id=Column(Integer,primary_key=True)
    status_code=Column(Integer,nullable=False)
    requests = Column(Text, nullable=True)  # Gelen isteğin JSON'u (hassas veriler temizlenmiş)
    response = Column(Text, nullable=True)  # Giden yanıtın JSON'u (hassas veriler temizlenmiş)
    error_message = Column(Text, nullable=True)
    created_at=Column(DateTime,default=datetime.datetime.now)

    message_id=Column(Integer,ForeignKey("message.id"),nullable=False)
    message=relationship("MessageModel",back_populates="logs")

