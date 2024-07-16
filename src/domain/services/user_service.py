from src.app.dependencies.repositories import IUserRepository
from src.domain.schemas.user_schema import UserReadSchema


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.__user_repository = user_repository

    async def get_users(self, skip: int, limit: int) -> list[UserReadSchema]:
        users = await self.__user_repository.read_many(
            order="date_of_birth", offset=skip, limit=limit
        )
        return [
            UserReadSchema.model_validate(user, from_attributes=True) for user in users
        ]

    async def get_subscribed_users(self, subscriber_id: int) -> list[UserReadSchema]:
        subscribed_to = await self.__user_repository.get_subscribed_users(subscriber_id)
        return [
            UserReadSchema.model_validate(user, from_attributes=True)
            for user in subscribed_to
        ]

    async def get_subscribers_for_user(
        self, subscribed_to_id: int
    ) -> list[UserReadSchema]:
        subscribers = await self.__user_repository.get_subscribers_for_user(
            subscribed_to_id
        )
        return [
            UserReadSchema.model_validate(user, from_attributes=True)
            for user in subscribers
        ]
