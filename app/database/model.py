from sqlalchemy import JSON, Column
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timedelta, timezone
import secrets


class User(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    hashed_password: str = Field(min_length=5, max_length=1024)
    email: str = Field(unique=True, index=True)
    users: list["AccessToken"] = Relationship(back_populates="user")


class UserRegister(SQLModel):
    name: str
    password: str
    email: str


class AccessToken(SQLModel, table=True):
    access_token: str = Field(primary_key=True, default_factory=lambda: generate_token(), max_length=1024, nullable=False)
    expiration_date: datetime = Field(default_factory=lambda: get_expiration_date(), nullable=False)
    user_id:int = Field(foreign_key="user.id", nullable=False)
    user: User|None = Relationship(back_populates="users")


class Thirukural(SQLModel, table=True):
    id: int|None = Field(primary_key=True, default=None)
    kural_no: int = Field(index=True) 
    adhikarm_no: int = Field(index=True)
    pal_bamini: str
    pal_english: str
    pal_thanglish: str
    pal_tamil: str
    iyal_bamini: str
    iyal_english: str
    iyal_thanglish: str
    iyal_tamil: str
    adhikarm_bamini: str
    adhikarm_english: str
    adhikarm_thanglish: str
    adhikarm_tamil: str
    kural_bamini1: str
    kural_bamini2: str
    kural_thanglish1: str
    kural_thanglish2: str
    kuralvilakam_tamil: str
    kuralvilakam_english: str
    meta: dict = Field(sa_column=Column(JSON))




def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=duration_seconds)


def generate_token() -> str:
    return secrets.token_urlsafe(32)