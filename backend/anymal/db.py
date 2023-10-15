from typing import AsyncGenerator, List

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase, SQLAlchemyBaseOAuthAccountTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase, SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from .config import settings

DATABASE_URL = settings.db_url

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model inheriting from FastAPI users base User model."""
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """Model representing access tokens with UUID as primary key."""
    pass

async def create_db_and_tables():
    """
    Asynchronously create database and tables.
    Note: Use cautiously to avoid unintentional DB resets in production.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Generate an asynchronous database session.

    Yields:
        AsyncSession: SQLAlchemy AsyncSession object.
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    """
    Provide an access token database instance.
    Args:
        session (AsyncSession): An asynchronous session with the database.
    Yields:
        SQLAlchemyAccessTokenDatabase: An instance interfacing the access token database.
    """
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


