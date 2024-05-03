from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    last_login = Column(TIMESTAMP(timezone=True))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    role = Column(String(50), default="user")
    failed_login_attempts = Column(Integer, default=0)
    last_failed_login = Column(TIMESTAMP(timezone=True))
    password_changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    reset_token = Column(Text)
    reset_token_expires_at = Column(TIMESTAMP(timezone=True))
    two_factor_secret = Column(Text)
    two_factor_enabled = Column(Boolean, default=False)
    last_updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Update the relationship if necessary
    # items = relationship("Item", back_populates="owner")
