from typing import Generic, Type, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.exceptions import DBIntegrityError
from src.infra.models.base_model import Base
from src.infra.repositories.base_repository import IRepository

ModelType = TypeVar("ModelType", bound=Base)


class SQLAlchemyRepository(IRepository, Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def create_one(self, data: dict) -> ModelType:
        try:
            instance = self.model(**data)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
        except IntegrityError:
            raise DBIntegrityError(self.model.__name__)
        else:
            return instance

    async def read_one(self, **filters) -> ModelType | None:
        res = await self.session.execute(select(self.model).filter_by(**filters))
        return res.scalar_one_or_none()

    async def read_many(
        self, order: str = "id", limit: int = 100, offset: int = 0
    ) -> list[ModelType]:
        res = await self.session.execute(
            select(self.model).order_by(order).offset(offset).limit(limit)
        )
        return res.scalars().all()

    async def delete(self, **filters) -> None:
        await self.session.execute(delete(self.model).filter_by(**filters))
        await self.session.commit()
