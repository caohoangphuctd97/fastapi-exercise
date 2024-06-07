from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.schemas import APIKeyResponse
from app.controllers.user import create_api_key, get_user_by_id, delete_user
from app.exceptions.configure_exceptions import UserNotFound
from app.database.depends import create_session
from app.utils.authentication import AuthenticationAdminRole
import logging
import secrets
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="",
    tags=["users"]
)
authentication_admin_role = AuthenticationAdminRole()
logger = logging.getLogger("__main__")


from fastapi import HTTPException
from app.schemas import SignUpReq, SignUpRes
from app.controllers.user import create_user
from app.utils.authentication import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

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
