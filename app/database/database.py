from copy import deepcopy
from sqlmodel import Session, create_engine, select
import os
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from .model import User, AccessToken, Thirukural
from .auth import verify_password
from settings import Settings

app_settings = Settings()
db_file_name = app_settings.db_filename
#db_file_name = "kural.db"
db_url = f"sqlite:///{db_file_name}"
connect_args = {"check_same_thread": False}


#if os.path.isfile(db_file_name):
#    db_url = "sqlite:///:memory:"

engine = create_engine(db_url, connect_args=connect_args, echo=False)

session = Session(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()



def get_session():
    with Session(engine) as session:
        yield session



def authenticate(email: str, passwd: str, db: Session) -> User|None:
    query = select(User).where(User.email == email)
    result = db.exec(query)
    user: User|None = result.first()

    if user is None:
        return None
    
    if not verify_password(passwd, user.hashed_password):
        return None
    
    return user


def create_access_token(user: User, db: Session) -> AccessToken:
    access_token = AccessToken(user_id=user.id)
    db.add(access_token)
    db.commit()
    return access_token


def get_user(user_id: int) -> User:
    st = select(User).where(id=user_id)
    user : User|None = session.exec(st).first()
    return user


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")),
                     db: Session = Depends(get_session)):
    query = select(AccessToken).where(AccessToken.access_token==token, 
            AccessToken.expiration_date >= datetime.now(tz=timezone.utc)
        )
    result = db.exec(query)
    access_token: AccessToken | None = result.first()

    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return access_token.user



def get_user_by_email(email:str) -> User:
    st = select(User).where(User.email==email)
    user : User|None = session.exec(st).first()
    return user    


from sqlalchemy import func

def check_kural_data() -> int:
    st = select(func.count(Thirukural.id))
    return session.exec(st).one()
    #return count