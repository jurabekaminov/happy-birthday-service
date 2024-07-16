import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from src.domain.email_utils.email_config import email_settings
from src.domain.schemas.notification_schema import NotificationSchema

logger = logging.getLogger(__name__)


class EmailHelper:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send_newsletter(self, notification_schema: NotificationSchema) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.user
        msg["To"] = ",".join(notification_schema.subscriber_emails)
        msg["Subject"] = "🎁 День рождения сотрудника! 🎁 "

        body = f"Сегодня день рождения у сотрудника: {notification_schema.name} {notification_schema.surname} ({notification_schema.email})!"  # noqa: E501, RUF001
        msg.attach(MIMEText(body, "plain"))

        with SMTP_SSL(self.host, self.port) as server:
            server.login(self.user, self.password)
            server.send_message(msg)

        logger.info(
            "Notification about user: %s was sent to %s",
            notification_schema.email,
            notification_schema.subscriber_emails,
        )


email_helper = EmailHelper(
    email_settings.HOST,
    email_settings.PORT,
    email_settings.USER,
    email_settings.PASSWORD,
)
