from datetime import datetime

from sqlalchemy import Column, Text, DateTime, Integer
from sqlalchemy.dialects import postgresql as pg

from .config import BaseMixin, BaseModel


class Users(BaseMixin, BaseModel):    # type: ignore
    id = Column(
        'id', pg.UUID, nullable=False, primary_key=True)
    email = Column(Text, nullable=False)
    password = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    modified_at = Column(DateTime, default=datetime.now, nullable=True)
