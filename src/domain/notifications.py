import logging
from datetime import date, datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.app.app_config import app_settings
from src.domain.email_utils.email_helper import email_helper
from src.domain.schemas.notification_schema import NotificationSchema
from src.infra.db.db_helper import db_helper
from src.infra.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class NotificationsHandler:
    def __init__(self):
        self.__scheduler = AsyncIOScheduler(timezone=app_settings.TZ)
        self.__session_factory = db_helper.get_session_factory()

    def get_scheduler(self) -> AsyncIOScheduler:
        self.__scheduler.add_job(
            func=self.send_notifications,
            trigger="cron",
            hour=5,
            minute=0,
        )
        return self.__scheduler

    async def __get_birthday_users_subscribers(
        self, birthday: date
    ) -> list[NotificationSchema]:
        """Gets users that were born date with of subscriber emails.

        Args:
        ----
            birthday (date): date of birth.

        Returns:
        -------
            birthday_info (list[NotificationSchema]): Bday boys with subscribers emails.

        """
        birthday_info: list[NotificationSchema] = []
        async with self.__session_factory() as session:
            user_repository = UserRepository(session)
            bday_boys = await user_repository.get_users_by_date_of_birth(birthday)
            for bday_boy in bday_boys:
                subs_emails = [user.email for user in bday_boy.subscribers]
                if not subs_emails:
                    continue
                birthday_info.append(
                    NotificationSchema(
                        name=bday_boy.name,
                        surname=bday_boy.surname,
                        email=bday_boy.email,
                        subscriber_emails=subs_emails,
                    )
                )
            return birthday_info

    async def send_notifications(self) -> None:
        today = datetime.now(tz=app_settings.TZ).date()
        birthday_info = await self.__get_birthday_users_subscribers(today)
        for info in birthday_info:
            logger.info("Sending notifications about %s to all subscribers", info.email)
            email_helper.send_newsletter(info)


notifications_handler = NotificationsHandler()
