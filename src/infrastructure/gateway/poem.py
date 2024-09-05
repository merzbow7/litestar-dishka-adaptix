from collections.abc import Iterable
from uuid import UUID

from adaptix.conversion import get_converter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from application.dto import PoemDTO

from application.interface import PoemReaderInterface, AuthorPoemReader
from infrastructure.models import Poem


class PoemGateway(PoemReaderInterface, AuthorPoemReader):

    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def read_by_uuid(self, uuid: UUID) -> PoemDTO | None:
        stmt = select(Poem).where(Poem.uuid == uuid)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            convert_poem_to_dto = get_converter(Poem, PoemDTO)
            return convert_poem_to_dto(row)
        return None

    @override
    async def read_by_author_uuid(self, uuid: UUID) -> PoemDTO | None:
        stmt = select(Poem).where(Poem.author_uuid == uuid)
        result = await self._session.execute(stmt)
        row = result.scalars()
        if row:
            convert_poems_to_dto = get_converter(Iterable[Poem], list[PoemDTO])
            return convert_poems_to_dto(row)
        return None
