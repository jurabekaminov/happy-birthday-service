from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base_model import Base
from src.infra.models.mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(64))
    surname: Mapped[str] = mapped_column(String(64))
    patronymic: Mapped[str] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password_hashed: Mapped[str] = mapped_column(String(256))
    date_of_birth: Mapped[date] = mapped_column(Date, index=True)

    # Relationships
    subscriptions: Mapped[list["User"]] = relationship(
        "User",
        secondary="subscriptions",
        primaryjoin="Subscription.subscriber_id==User.id",
        secondaryjoin="Subscription.subscribed_to_id==User.id",
        back_populates="subscribers",
        lazy="selectin",
        overlaps="subscriber",
        viewonly=True
    )
    subscribers: Mapped[list["User"]] = relationship(
        "User",
        secondary="subscriptions",
        primaryjoin="Subscription.subscribed_to_id==User.id",
        secondaryjoin="Subscription.subscriber_id==User.id",
        back_populates="subscriptions",
        lazy="selectin",
        overlaps="subscribed_to",
        viewonly=True
    )
