import logging
import datetime
import uuid
from typing import List

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users, Post
from app.schemas import CreatePostRes
from app.exceptions.configure_exceptions import UserExisted


logger = logging.getLogger("__main__")

async def create_post(db: AsyncSession, text: str, user: Users) -> Post:
    new_post = Post(
        text=text,
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now(),
        user_id=user.id
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


async def get_posts_by_user_id(db: AsyncSession, user_id: bytes) -> List[CreatePostRes]:
    posts = await db.execute(select(Post).where(Post.user_id == user_id))
    return posts.scalars().all()


async def get_post_by_user_id_and_post_id(db: AsyncSession, user_id: bytes, post_id: bytes) -> CreatePostRes:
    post = await db.execute(
        select(Post).where(
            and_(
                Post.user_id == user_id,
                Post.id == post_id
            )
        )
    )
    return post.scalars().first()


async def delete_post_by_id(db: AsyncSession, post_id: uuid.UUID):
    post = await db.execute(select(Post).where(Post.id == post_id))
    post = post.scalars().first()
    if post:
        await db.delete(post)
        await db.commit()
