from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.db_helper import db_helper

ISession = Annotated[AsyncSession, Depends(db_helper.get_session)]
