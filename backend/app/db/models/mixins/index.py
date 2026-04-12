"""Reusable mixins for database models."""

from uuid import UUID

from sqlalchemy import Uuid, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """Mixin that provides a UUID primary key."""

    __abstract__ = True
    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, default=func.gen_random_uuid()
    )

    @classmethod
    async def find_by_id(cls, session: AsyncSession, entity_id: UUID):
        """Retrieve an entity by its UUID."""
        return await session.scalar(select(cls).where(cls.id == entity_id))
