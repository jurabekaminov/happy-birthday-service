from src.app.dependencies.session import ISession
from src.infra.models.subscription_model import Subscription
from src.infra.repositories.sqlalchemy_repository import SQLAlchemyRepository


class SubscriptionRepository(SQLAlchemyRepository):
    def __init__(self, session: ISession) -> None:
        super().__init__(Subscription, session)
