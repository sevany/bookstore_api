from pydantic import BaseModel
import enum
from fastapi import Query


class Role(enum.Enum):
    admin = "admin"
    personel = "personel"


class User(BaseModel):
    name: str   
    password: str
    mail: str = Query(None, regex="^([a-zA-Z0-9 \-\.]+)@([a-zA-Z0-9 \-\.]+)\.(a-zA-Z]{2,5})$")

    role: Role
