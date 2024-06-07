from fastapi import APIRouter, status, Depends
from app.database.depends import create_session
from app.utils.authentication import AuthenticationRole
import logging
import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import SignUpReq, SignUpRes, CreatePostReq, CreatePostRes
from app.database.models import Users
from app.controllers.user import create_user, get_user_by_email
from app.controllers.post import (
    create_post, get_posts_by_user_id, delete_post_by_id, get_post_by_user_id_and_post_id
)
from app.utils.authentication import create_access_token, verify_password, get_password_hash

router = APIRouter(
    prefix="",
    tags=["users"]
)
authentication = AuthenticationRole()
logger = logging.getLogger("__main__")


@router.post("/signup", response_model=SignUpRes, status_code=status.HTTP_201_CREATED)
async def signup(form_data: SignUpReq, db: AsyncSession = Depends(create_session)):
    user = await create_user(db, form_data.email, get_password_hash(form_data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/signin", response_model=SignUpRes)
async def signin(form_data: SignUpReq, db: AsyncSession = Depends(create_session)):
    user = await get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/post", response_model=CreatePostRes, status_code=status.HTTP_201_CREATED)
async def create_post_api(
    post_data: CreatePostReq, db: AsyncSession = Depends(create_session),
    user: Users = Depends(authentication)
):
    post = await create_post(db, post_data.text, user)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post could not be created",
        )
    return post


@router.get("/post", status_code=status.HTTP_200_OK, response_model=List[CreatePostRes])
async def get_post(
    db: AsyncSession = Depends(create_session), user: Users = Depends(authentication)
):
    posts = await get_posts_by_user_id(db, user.id)
    if len(posts) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return posts


@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: uuid.UUID, db: AsyncSession = Depends(create_session),
    user: Users = Depends(authentication)
):
    post = await get_post_by_user_id_and_post_id(db, user.id, post_id.bytes)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    await delete_post_by_id(db, post_id)
    return {"message": "Post deleted successfully"}
