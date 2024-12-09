from fastapi import APIRouter, HTTPException, Body, Depends, Request

from ..domain.user.models import DBUser
from ..domain.user.schemas import (
    RegisterUser,
    LoginUser,
    TokenResponse,
    UserInfoResponse,
)

from ..domain.user.service import find_user, get_user, insert_user, hash_password, verify_password
from ..dependencies import create_jwt_token

from ..domain.config import AccessLevel
from ..dependencies import JWTBearer, get_user_id

user_router = APIRouter(tags=["user"])


@user_router.post("/user/auth/register")
async def register_user(user: RegisterUser = Body()) -> TokenResponse:
    username = user.username
    password = user.password
    email = user.email
    hashed_password = hash_password(password)

    found_user = await find_user({"username": username})
    if found_user:
        raise HTTPException(status_code=409, detail="User already exists")
    else:
        # TODO: make it modify only the hashed password field and access_level
        user_entry = DBUser(
            username=username,
            hashed_password=hashed_password,
            email=email,
            access_level=AccessLevel.default,
        )
        result = await insert_user(user_entry)

        if result:
            jwt_token = create_jwt_token(
                username=username,
                user_id=str(result.id),
                scope=str(AccessLevel.default),
            )
            return {"access_token": jwt_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")

# TODO: rework to make data transfer in headers
@user_router.post("/user/auth/login")
async def login_user(user: LoginUser = Body()) -> TokenResponse:
    username = user.username
    password = user.password
    email = user.email

    found_user = await find_user({"username": username})
    if not found_user:
        raise HTTPException(status_code=404, detail="User is not registered")
    else:
        if verify_password(password, found_user.hashed_password):
            jwt_token = create_jwt_token(
                username=username,
                user_id=str(found_user.id),
                scope=found_user.access_level,
            )
            return {"access_token": jwt_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Wrong password")



@user_router.post("/user/info", dependencies=[Depends(JWTBearer())])
async def get_user_info(user_id: str = Depends(get_user_id)) -> UserInfoResponse:
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User is not registered")
    else:
        return UserInfoResponse.model_validate(user)