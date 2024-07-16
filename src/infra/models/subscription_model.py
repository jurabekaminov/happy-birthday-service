from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base_model import Base

if TYPE_CHECKING:
    from src.infra.models.user_model import User


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint("subscriber_id != subscribed_to_id", name="check_not_self_sub"),
        UniqueConstraint("subscriber_id", "subscribed_to_id", name="unique_subs"),
    )

    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    subscribed_to_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
    )

    # Relationships
    subscriber: Mapped["User"] = relationship(
        "User",
        foreign_keys=[subscriber_id],
        lazy="selectin",
        viewonly=True
    )
    subscribed_to: Mapped["User"] = relationship(
        "User",
        foreign_keys=[subscribed_to_id],
        lazy="selectin",
        viewonly=True
    )
