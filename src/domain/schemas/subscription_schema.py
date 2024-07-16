from datetime import datetime

from pydantic import BaseModel

from src.domain.schemas.user_schema import UserReadSchema


class SubscriptionReadSchema(BaseModel):
    subsrciber: UserReadSchema
    subscribed_to: UserReadSchema
    created_at: datetime
