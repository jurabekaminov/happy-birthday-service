from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.dependencies.services import IAuthService
from src.domain.schemas.token_schema import TokenSchema
from src.domain.schemas.user_schema import UserCreateSchema, UserReadSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenSchema)
async def login(
    schema: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: IAuthService,
):
    token = await service.login(schema.username, schema.password)
    return token


@router.post(
    "/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def register(schema: UserCreateSchema, service: IAuthService):
    user = await service.register(schema)
    return user
