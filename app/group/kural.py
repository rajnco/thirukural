from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlmodel import Session, select
from fastapi.security import APIKeyHeader
import random


from database.database import get_db, get_current_user
from database.model import Thirukural, User
from security import get_current_jwt_user
from settings import Settings, get_settings

kural_router = APIRouter()
kural_router2 = APIRouter()

api_key_header = APIKeyHeader(name="Token")


@kural_router.get("/kural/by/id/plain/{kural_no}", tags=["Kural"])
async def get_kural_by_id_plain(kural_no: int, db: Session = Depends(get_db)):
    st = select(Thirukural).where(Thirukural.kural_no==kural_no)
    result = db.exec(st).first()
    return {"kural": result}


@kural_router.get("/kural/by/adhikarm/plain/{adhikarm_no}", tags=["Kural"])
async def get_kurals_by_adhikarm_plain(adhikarm_no: int, db:Session = Depends(get_db)):
    st = select(Thirukural).where(Thirukural.adhikarm_no==adhikarm_no)
    return {"kurals": db.exec(st).all()}


@kural_router.get("/kural/by/id/plain/random/", tags=["Kural"])
async def get_kural_by_id_plain_random(kural_no: int|None = None,
                                       db: Session = Depends(get_db)):
    if not kural_no:
        kural_no = random.randint(0, 1331)    
    st = select(Thirukural).where(Thirukural.kural_no==kural_no)
    result = db.exec(st).first()
    return {"kural": result}



@kural_router.get("/kural/by/adhikarm/plain/random/", tags=["Kural"])
async def get_kurals_by_adhikarm_plain_random(adhikarm_no: int|None = None, 
                                              db:Session = Depends(get_db)):
    if not adhikarm_no:
        adhikarm_no = random.randint(0,134)
    st = select(Thirukural).where(Thirukural.adhikarm_no==adhikarm_no)
    return {"kurals": db.exec(st).all()}



@kural_router.get("/kural/by/id/apikey/{kural_no}", tags=["Kural By APIKey in Header"])
async def get_kural_by_id_apikey(kural_no: int, db: Session = Depends(get_db), apikey:str = Depends(api_key_header), app_settings:Settings = Depends(get_settings)):
    if apikey != app_settings.api_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    st = select(Thirukural).where(Thirukural.kural_no==kural_no)
    result = db.exec(st).first()
    return {"kural": result}


@kural_router.get("/kural/by/adhikarm/apikey/{adhikarm_no}", tags=["Kural By APIKey in Header"])
async def get_kurals_by_adhikarm_apikey(adhikarm_no: int, db:Session = Depends(get_db), apikey:str = Depends(api_key_header), app_settings: Settings = Depends(get_settings)):
    if apikey != app_settings.api_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    st = select(Thirukural).where(Thirukural.adhikarm_no==adhikarm_no)
    return {"kurals": db.exec(st).all()}



@kural_router.get("/kural/by/id/jwt/{kural_no}", tags=["Kural By JWT Token"])
async def get_kural_by_id_jwt(kural_no: int, db: Session = Depends(get_db), user: User = Depends(get_current_jwt_user)):
    st = select(Thirukural).where(Thirukural.kural_no==kural_no)
    result = db.exec(st).first()
    return {"kural": result}


@kural_router.get("/kural/by/adhikarm/jwt/{adhikarm_no}", tags=["Kural By JWT Token"])
async def get_kurals_by_adhikarm_jwt(adhikarm_no: int, db:Session = Depends(get_db), user: User = Depends(get_current_jwt_user)):
    st = select(Thirukural).where(Thirukural.adhikarm_no==adhikarm_no)
    return {"kurals": db.exec(st).all()}


@kural_router2.get("/kural/by/id/usertoken/{kural_no}", tags=["Kural By User Token"])
async def get_kural_by_id_accesstoken(kural_no: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    st = select(Thirukural).where(Thirukural.kural_no==kural_no)
    result = db.exec(st).first()
    return {"kural": result}


@kural_router2.get("/kural/by/adhikarm/usertoken/{adhikarm_no}", tags=["Kural By User Token"])
async def get_kurals_by_adhikarm_accesstoken(adhikarm_no: int, db:Session = Depends(get_db), user: User = Depends(get_current_user)):
    st = select(Thirukural).where(Thirukural.adhikarm_no==adhikarm_no)
    return {"kurals": db.exec(st).all()}

