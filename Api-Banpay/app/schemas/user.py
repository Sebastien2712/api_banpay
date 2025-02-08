from pydantic import BaseModel
from enum import Enum
from typing import Optional


class RoleEnum(str, Enum):
    admin = "admin"
    films = "films"
    people = "people"
    locations = "locations"
    species = "species"
    vehicles = "vehicles"

class UserBase(BaseModel):
    username: str
    email: str
    role: RoleEnum

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None  
    role: Optional[str] = None    