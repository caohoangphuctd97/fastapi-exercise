from typing import List, Optional
from datetime import datetime
import uuid

from pydantic import (
    BaseModel, Field, NonNegativeInt, EmailStr)


class UserSchema(BaseModel):
    user_id: uuid.UUID = Field(..., alias="id")
    email: EmailStr
    password: str
    created_at: datetime
    modified_at: datetime

    class Config:
        populate_by_name = True
        extra = 'forbid'
        from_attributes = True

class SignUpReq(BaseModel):
    email: EmailStr
    password: str

class SignUpRes(BaseModel):
    access_token: str
    token_type: str
