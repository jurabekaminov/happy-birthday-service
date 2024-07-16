from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.domain.schemas.token_schema import TokenPayloadSchema, TokenSchema
from src.domain.token_utils.token_config import jwt_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenHelper:
    @staticmethod
    def verify_password(text_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(text_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_token(payload: TokenPayloadSchema) -> TokenSchema:
        access_token = jwt.encode(
            payload.model_dump(),
            key=jwt_settings.SECRET_KEY,
            algorithm=jwt_settings.ALGORITHM,
        )
        return TokenSchema(access_token=access_token, token_type="bearer")

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)) -> TokenPayloadSchema:
        try:
            payload = jwt.decode(
                token,
                key=jwt_settings.SECRET_KEY,
                algorithms=[jwt_settings.ALGORITHM]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenPayloadSchema.model_validate(payload)
