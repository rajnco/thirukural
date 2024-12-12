from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
import datetime
from fastapi.security import OAuth2PasswordBearer

from database.database import  get_user_by_email
from database.model import User
from settings import Settings, get_settings

app_settings = get_settings()

def create_jwt_access_token(data: dict) -> str:
    encode_data = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=app_settings.access_token_expire_minutes)
    encode_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encode_data, app_settings.secret_key, algorithm=app_settings.algorithm)
    return encoded_jwt

def decode_jwt_access_token(token:str) -> User|None:
    try: 
        payload = jwt.decode(token, app_settings.secret_key, algorithms=[app_settings.algorithm])
        username: str = payload.get("sub")
    except JWTError:
        return
    if not username: 
        return
    user = get_user_by_email(username) # username is email-id
    return user



def get_current_jwt_user(token:str=Depends(OAuth2PasswordBearer(tokenUrl="jwt_token"))):
    user = decode_jwt_access_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return user
