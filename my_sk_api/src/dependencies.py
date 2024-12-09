import os
import jwt

from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = os.environ["JWT_ALG"]
EXP_TIME_MINUTES = int(os.environ["JWT_EXP_TIME_MINUTES"])


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

def get_user_id(token: str = Depends(JWTBearer())) -> str:
    return get_user_id_from_jwt(token)


def encode_jwt_token(payload: dict, expire: datetime, scope: str) -> str:
    payload = payload
    payload["exp"] = expire
    payload["scope"] = scope

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, ALGORITHM)


def verify_jwt_token(token: str) -> bool:
    try:
        decode_jwt_token(token)
        return True
    except:
        return False


def create_jwt_token(
    username: str, user_id: str, scope: str, exp_time: timedelta | None = None
) -> str:
    payload = {"sub": username}
    payload = {"uid": user_id}
    if exp_time:
        expire = datetime.now(timezone.utc) + exp_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXP_TIME_MINUTES)

    token = encode_jwt_token(payload=payload, expire=expire, scope=scope)

    return token


def get_data_from_jwt(token: str, claims: list[str]) -> str | list[str]:
    decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
    return [decoded_token.get(claim, None) for claim in claims]


def get_user_id_from_jwt(token: str) -> str:
    return get_data_from_jwt(token=token, claims=["sub"])[0]


def get_user_id_from_jwt(token: str) -> str:
    return get_data_from_jwt(token=token, claims=["uid"])[0]


def get_user_data_from_jwt(token: str) -> str:
    return get_data_from_jwt(token=token, claims=["uid", "sub"])
