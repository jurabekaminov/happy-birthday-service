from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infra.db.db_config import db_settings


class DBHelper:
    def __init__(self, url: str, echo: bool = False):
        self.__engine = create_async_engine(url=url, echo=echo)
        self.__session_factory = async_sessionmaker(
            bind=self.__engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session_factory(self) -> async_sessionmaker:
        return self.__session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.__session_factory() as session:
            yield session


db_helper = DBHelper(db_settings.connection_string, db_settings.ECHO)
