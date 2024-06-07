from fastapi import APIRouter, status, Depends
from app.database.depends import create_session
from app.utils.authentication import AuthenticationAdminRole
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas import SignUpReq, SignUpRes
from app.controllers.user import create_user
from app.utils.authentication import create_access_token

router = APIRouter(
    prefix="",
    tags=["users"]
)
authentication_admin_role = AuthenticationAdminRole()
logger = logging.getLogger("__main__")


@router.post("/signup", response_model=SignUpRes, status_code=status.HTTP_201_CREATED)
async def signup(form_data: SignUpReq, db: AsyncSession = Depends(create_session)):
    user = await create_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signin", response_model=SignUpRes)
async def signin(form_data: SignUpReq, db: AsyncSession = Depends(create_session)):
    user = await get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostReq, db: AsyncSession = Depends(create_session)):
    post = await create_post(db, post_data.title, post_data.content, post_data.author_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post could not be created",
        )
    return {"message": "Post created successfully"}


@router.get("/post", status_code=status.HTTP_200_OK)
async def get_post(db: AsyncSession = Depends(create_session)):
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: AsyncSession = Depends(create_session)):
    post = await get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    await delete_post_by_id(db, post_id)
    return {"message": "Post deleted successfully"}
