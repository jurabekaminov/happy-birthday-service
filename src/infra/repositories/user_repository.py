from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.app.dependencies.session import ISession
from src.infra.models.user_model import User
from src.infra.repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self, session: ISession) -> None:
        super().__init__(User, session)

    async def get_subscribed_users(self, subscriber_id: int) -> list[User]:
        res = await self.session.execute(select(User).filter_by(id=subscriber_id))
        user = res.scalar_one_or_none()
        if user is None:
            return []
        await self.session.refresh(user)
        return user.subscriptions

    async def get_subscribers_for_user(self, subscribed_to_id: int) -> list[User]:
        res = await self.session.execute(select(User).filter_by(id=subscribed_to_id))
        user = res.scalar_one_or_none()
        if user is None:
            return []
        await self.session.refresh(user)
        return user.subscribers

    async def get_users_by_date_of_birth(self, date_of_birth: date) -> list[User]:
        res = await self.session.execute(
            select(User)
            .options(selectinload(User.subscribers))
            .filter_by(date_of_birth=date_of_birth)
        )
        return res.scalars().all()
