from datetime import datetime
from pydantic import BaseModel


class JWTTokenData(BaseModel):
    payload: dict
    expire: datetime
    scope: str


class JWTToken(BaseModel):
    access_token: str
