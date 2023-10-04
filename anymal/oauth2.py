from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings
from .schemas import auth as auth_schema
from . import database, models

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl='sign-in'
)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.hashing_algorithm
ACCESS_TOKEN_EXPIRE_DAYS = settings.access_token_expire_days

def create_access_token(
        data: dict
    ):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire})
    access_token = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )
    return access_token

def verify_access_token(
        access_token: str,
        token_exception: JWTError
    ):
    try:
        payload = jwt.decode(
            token=access_token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get('user_id')
        if user_id is None:
            raise token_exception
        token_data = auth_schema.TokenData(user_id=user_id)
    except JWTError:
        raise token_exception
    return token_data

def get_current_user(
        access_token: str=Depends(oauth2_schema),
        db: Session=Depends(database.dbc)
    ):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    token_data = verify_access_token(
        access_token=access_token,
        token_exception=token_exception
    )
    current_user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    return current_user
