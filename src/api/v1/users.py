from fastapi import APIRouter

from src.app.dependencies.api import CommonsDep
from src.app.dependencies.auth import IUserInfo
from src.app.dependencies.services import IUserService
from src.domain.schemas.user_schema import UserReadSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserReadSchema])
async def get_users(
    _: IUserInfo,
    service: IUserService,
    commons: CommonsDep,
):
    users = await service.get_users(commons["skip"], commons["limit"])
    return users


@router.get("/me/subscriptions", response_model=list[UserReadSchema])
async def get_my_subscriptions(
    user_info: IUserInfo,
    service: IUserService,
):
    subscribed_by_me = await service.get_subscribed_users(int(user_info.sub))
    return subscribed_by_me


@router.get("/me/subscribers", response_model=list[UserReadSchema])
async def get_my_subscribers(
    user_info: IUserInfo,
    service: IUserService,
):
    subscribers = await service.get_subscribers_for_user(int(user_info.sub))
    return subscribers
