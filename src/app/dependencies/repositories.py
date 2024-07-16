from typing import Annotated

from fastapi import Depends

from src.infra.repositories.subscription_repository import SubscriptionRepository
from src.infra.repositories.user_repository import UserRepository

IUserRepository = Annotated[UserRepository, Depends()]
ISubscriptionRepository = Annotated[SubscriptionRepository, Depends()]
