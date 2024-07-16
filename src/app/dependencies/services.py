from typing import Annotated

from fastapi import Depends

from src.domain.services.auth_service import AuthService
from src.domain.services.subscription_service import SubscriptionService
from src.domain.services.user_service import UserService

IAuthService = Annotated[AuthService, Depends()]
IUserService = Annotated[UserService, Depends()]
ISubscriptionService = Annotated[SubscriptionService, Depends()]
