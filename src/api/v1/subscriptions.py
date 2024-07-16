from fastapi import APIRouter, BackgroundTasks, status

from src.app.dependencies.auth import IUserInfo
from src.app.dependencies.services import ISubscriptionService
from src.domain.schemas.subscription_schema import SubscriptionReadSchema

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post(
    "", response_model=SubscriptionReadSchema, status_code=status.HTTP_201_CREATED
)
async def subscribe(
    subscriber_info: IUserInfo,
    subscribe_to_id: int,
    service: ISubscriptionService,
    background_tasks: BackgroundTasks,
):
    subscription = await service.subscribe(
        int(subscriber_info.sub), subscribe_to_id, background_tasks
    )

    return subscription


@router.delete("")
async def unsubscribe(
    subscriber_info: IUserInfo, unsubscribe_to_id: int, service: ISubscriptionService
):
    await service.unsubscribe(int(subscriber_info.sub), unsubscribe_to_id)
    return {"detail": "Subscription deleted."}
