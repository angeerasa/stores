from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum as SQLEnum,CheckConstraint
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from datetime import timedelta, datetime, timezone

class UserRolesEnum(PyEnum):
    customer = "customer"
    owner = "owner"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    mobile: Mapped[str] = mapped_column(String(10), CheckConstraint("mobile ~ '^[0-9]{10}$'", name="ck_users_mobile_10Digits"), nullable=False)
    role: Mapped[UserRolesEnum] = mapped_column(SQLEnum(UserRolesEnum, name = "user_roles_enum"), nullable=False, server_default="customer")
    last_login: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_loggedin: Mapped[bool] = mapped_column(Boolean, server_default="False")

class Otp(Base):
    __tablename__="otp"
    mobile: Mapped[str] = mapped_column(String(10), CheckConstraint("mobile ~ '^[0-9]{10}$'", name="ck_users_mobile_10Digits"), nullable=False, primary_key=True)
    otp: Mapped[str] = mapped_column(String(4));
    expiry_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(minutes=2), onupdate=lambda: datetime.now(timezone.utc) + timedelta(minutes=2))


