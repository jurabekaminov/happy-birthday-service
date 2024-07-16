from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    iat: datetime
    exp: datetime
    sub: str
    email: str
