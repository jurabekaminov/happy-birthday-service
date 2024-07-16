from typing import Annotated

from fastapi import Depends

from src.domain.schemas.token_schema import TokenPayloadSchema
from src.domain.token_utils.token_helper import TokenHelper

IUserInfo = Annotated[TokenPayloadSchema, Depends(TokenHelper.verify_token)]
