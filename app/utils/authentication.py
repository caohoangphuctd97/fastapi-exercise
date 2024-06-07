import logging
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, status, Depends
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.requests import Request
from app.config import config
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.user import get_user_by_email
from app.database.depends import create_session
from app.database.models import Users

logger = logging.getLogger("__main__")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)



async def authenticate_basic(
    request: Request
) -> HTTPAuthorizationCredentials:
    authorization = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    if not (authorization and scheme and credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="InvalidScheme"
        )
    return HTTPAuthorizationCredentials(
        scheme=scheme, credentials=credentials
    )


class AuthenticationRole(HTTPBearer):
    async def __call__(
        self, request: Request, db: AsyncSession = Depends(create_session)
    ) -> Users:
        credential: HTTPAuthorizationCredentials = (
            await authenticate_basic(request)
        )
        try:
            payload = jwt.decode(credential.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            user = await get_user_by_email(db, payload.get('sub'))
            if user:
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="InvalidUser"
                )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="InvalidToken"
            )
