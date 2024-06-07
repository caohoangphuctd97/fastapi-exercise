import logging
import datetime
import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users
from app.schemas import UserSchema
from app.exceptions.configure_exceptions import UserExisted


logger = logging.getLogger("__main__")


async def create_user(db: AsyncSession, email: str, password: str) -> UserSchema:
    user = await db.execute(select(Users).where(Users.email == email))
    user = user.scalars().first()
    if user:
        raise UserExisted()

    new_user = Users(
        email=email,
        password=password,
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now()
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_user_by_email(db: AsyncSession, email: str) -> UserSchema:
    user = await db.execute(select(Users).where(Users.email == email))
    return user.scalars().first()

