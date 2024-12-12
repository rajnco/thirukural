from sqlmodel import Session, select
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from security import create_jwt_access_token, get_current_jwt_user
from database.model import UserRegister, User
from database.auth import get_password_hash
from database.database import get_session, create_access_token
from database.database import authenticate
from database.database import get_current_user


user_router = APIRouter()
user_router2 = APIRouter()


@user_router.post("/register", tags=["Users"])
def register(user_reg: UserRegister, db: Session = Depends(get_session)) -> User:
    hashed_password = get_password_hash(user_reg.password)
    user = User(name=user_reg.name,email=user_reg.email,hashed_password=hashed_password)
    try: 
        db.add(user)
        db.commit()
        db.refresh(user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= e.with_traceback)
    return user



@user_router2.post("/token", tags=["Users"])
def generate_token(form_data2: OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm), 
                   db: Session = Depends(get_session)):
    email = form_data2.username
    password = form_data2.password
    user =  authenticate(email, password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = create_access_token(user, db)
    return {"access_token": token.access_token, "token_type": "bearer"}



@user_router.get("/users", tags=["Users"])
def get_user(db: Session = Depends(get_session)):
    st = select(User)
    user : User|None = db.exec(st).all()
    return {"users": user }


@user_router.get("/user/{user_id}", tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_session)):
    st = select(User).where(User.id==user_id)
    user : User|None = db.exec(st).first()
    return {"user": user }

@user_router.put("/user/{user_id}", tags=["Users"])
def update_user(user_id: int, name: str|None, db: Session = Depends(get_session)):
    st = select(User).where(User.id==user_id)
    user : User|None = db.exec(st).first()
    if user != None:
        user.name=name
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"Updated User": user}


@user_router.delete("/user/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_session)):
    st = select(User).where(User.id==user_id)
    user : User|None = db.exec(st).first()
    if user != None:
        db.delete(user)
        db.commit
    return {'deleted user': user}



@user_router.get("/whoami", tags=["Users"])
def get_loggedin_user(user: User = Depends(get_current_user)):
    return {"User": user}




@user_router.post("/jwt_token", tags=["Users-JWT Token"])
def get_user_jwt_access_token(form_data: OAuth2PasswordRequestForm=Depends(),
                              db: Session = Depends(get_session)):
    email = form_data.username
    password = form_data.password
    user =  authenticate(email, password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_access_token(data={"sub": email})
    return {"access_token": jwt_token, "token_type": "bearer"}



@user_router.get("/who/am/{I}", tags=["Users"])
#def get_loggedin_user(user: User = Depends(get_current_user)):
def get_loggedin_user(user: User = Depends(get_current_jwt_user)):
    return {"User": user}

@user_router.get("/who/am/{i}", tags=["Users-JWT Token"])
def read_user_me(user: User=Depends(get_current_jwt_user)):
    return { "description": f"{user.name} authorized"}
