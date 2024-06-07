import uuid
from datetime import datetime

from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship

from .config import BaseMixin, BaseModel


class Users(BaseMixin, BaseModel):    # type: ignore
    id = Column(
        'id', mysql.BINARY(16), default=uuid.uuid4().bytes, nullable=False, primary_key=True)
    email = Column(Text, nullable=False)
    password = Column(Text, default=0)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    modified_at = Column(DateTime, default=datetime.now, nullable=True)
    posts = relationship("Post", backref="user")


class Post(BaseMixin, BaseModel):
    id = Column(
        'id', mysql.BINARY(16), default=uuid.uuid4().bytes, nullable=False, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    modified_at = Column(DateTime, default=datetime.now, nullable=True)
    user_id = Column(mysql.BINARY(16), ForeignKey('users.id'), nullable=False)
