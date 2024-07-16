from pydantic import BaseModel, field_validator, validate_email


class NotificationSchema(BaseModel):
    name: str
    surname: str
    email: str
    subscriber_emails: list[str]

    @field_validator("subscriber_emails")
    @classmethod
    def check_email(cls, subscriber_emails: list[str]) -> list[str]:
        try:
            for recipient in subscriber_emails:
                _ = validate_email(recipient)
        except Exception as e:
            raise ValueError(e)
        return subscriber_emails
