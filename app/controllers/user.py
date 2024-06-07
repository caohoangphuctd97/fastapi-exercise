import logging
import datetime
import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users
from app.schemas import UserSchema
from app.exceptions.configure_exceptions import UserExisted


logger = logging.getLogger("__main__")


from sqlalchemy.exc import NoResultFound
from app.utils.authentication import get_password_hash

async def create_user(db: AsyncSession, email: str, password: str) -> UserSchema:
    user = await db.execute(select(Users).where(Users.email == email))
    user = user.scalars().first()
    if user:
        raise UserExisted()

    new_user = Users(
        id=uuid.uuid4(),
        email=email,
        password=get_password_hash(password),
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now()
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


