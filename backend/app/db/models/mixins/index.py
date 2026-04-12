from uuid import UUID

from sqlalchemy import Uuid, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    __abstract__ = True
    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, server_default=func.gen_random_uuid()
    )

    @classmethod
    async def find_by_id(cls, session: AsyncSession, entity_id: UUID):
        return await session.scalar(select(cls).where(cls.id == entity_id))
