from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model to store user-related data and states.

    Attributes:
        id: Unique identifier for the user.
        email: User's email address.
        password: User's password (Ensure this is hashed and secured properly).
        first_name: User's first name.
        last_name: User's last name.
        is_verified: Flag to indicate email verification status.
        created_at: Timestamp of when the user account was created.
        updated_at: Timestamp of the most recent update to the user account.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_verified = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
