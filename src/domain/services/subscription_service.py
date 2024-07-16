import logging
from datetime import datetime

from fastapi import BackgroundTasks, HTTPException, status

from src.app.app_config import app_settings
from src.app.dependencies.repositories import ISubscriptionRepository
from src.domain.email_utils.email_helper import email_helper
from src.domain.schemas.notification_schema import NotificationSchema
from src.domain.schemas.subscription_schema import SubscriptionReadSchema
from src.domain.schemas.user_schema import UserReadSchema
from src.infra.exceptions import DBIntegrityError

logger = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(self, subscription_repository: ISubscriptionRepository) -> None:
        self.__subscription_repository = subscription_repository

    async def send_email_if_needed(
        self,
        subscriber: UserReadSchema,
        subscribed_to: UserReadSchema,
        background_tasks: BackgroundTasks,
    ) -> None:
        today = datetime.now(tz=app_settings.TZ).date()
        if subscribed_to.date_of_birth != today:
            return
        notification_schema = NotificationSchema(
            name=subscribed_to.name,
            surname=subscribed_to.surname,
            email=subscribed_to.email,
            subscriber_emails=[subscriber.email],
        )
        background_tasks.add_task(email_helper.send_newsletter, notification_schema)
        

    async def subscribe(
        self,
        subscriber_id: int,
        subscribe_to_id: int,
        background_tasks: BackgroundTasks,
    ) -> SubscriptionReadSchema:
        if subscriber_id == subscribe_to_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot subscribe to yourself.",
            )
        try:
            new_subscription = await self.__subscription_repository.create_one(
                {"subscriber_id": subscriber_id, "subscribed_to_id": subscribe_to_id}
            )
            logger.info(
                "user (id=%s) subscribed to user (id=%s)",
                subscriber_id,
                subscribe_to_id,
            )
        except DBIntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Subscribing to user with id = {subscribe_to_id} provides integrity error.",  # noqa: E501
            )
        new_sub = SubscriptionReadSchema(
            subsrciber=UserReadSchema.model_validate(
                new_subscription.subscriber, from_attributes=True
            ),
            subscribed_to=UserReadSchema.model_validate(
                new_subscription.subscribed_to, from_attributes=True
            ),
            created_at=new_subscription.created_at,
        )
        await self.send_email_if_needed(
            new_sub.subsrciber, new_sub.subscribed_to, background_tasks
        )
        return new_sub

    async def unsubscribe(self, subscriber_id: int, unsubscribe_to_id: int) -> None:
        await self.__subscription_repository.delete(
            subscriber_id=subscriber_id, subscribed_to_id=unsubscribe_to_id
        )
        logger.info(
            "user (id=%s) unsubscribed to user (id=%s)",
            subscriber_id,
            unsubscribe_to_id,
        )
