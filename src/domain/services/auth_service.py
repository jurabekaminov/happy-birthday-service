from datetime import datetime, timedelta

from fastapi import HTTPException, status

from src.app.app_config import app_settings
from src.app.dependencies.repositories import IUserRepository
from src.domain.schemas.token_schema import TokenPayloadSchema, TokenSchema
from src.domain.schemas.user_schema import UserCreateSchema, UserReadSchema
from src.domain.token_utils.token_config import jwt_settings
from src.domain.token_utils.token_helper import TokenHelper
from src.infra.exceptions import DBIntegrityError


class AuthService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.__user_repository = user_repository

    async def register(self, user_schema: UserCreateSchema) -> UserReadSchema:
        user_dict = user_schema.model_dump()
        user_dict.pop("password_text")
        user_dict["password_hashed"] = TokenHelper.get_password_hash(
            user_schema.password_text
        )
        try:
            new_user = await self.__user_repository.create_one(user_dict)
        except DBIntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email: {user_schema.email} already exists.",
            )
        return UserReadSchema.model_validate(new_user, from_attributes=True)

    async def login(self, email: str, password_text: str) -> TokenSchema:
        user = await self.__user_repository.read_one(email=email)
        if not user or not TokenHelper.verify_password(
            password_text, user.password_hashed
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        now = datetime.now(tz=app_settings.TZ)
        payload = TokenPayloadSchema(
            iat=now,
            exp=now + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            sub=str(user.id),
            email=user.email,
        )
        return TokenHelper.create_token(payload)
