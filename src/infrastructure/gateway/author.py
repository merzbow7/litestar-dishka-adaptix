from collections.abc import Iterable
from uuid import UUID

from adaptix.conversion import get_converter
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from application.dto import AuthorDTO
from application.interface import AllAuthorReaderInterface
from application.interface.author import AuthorReaderInterface, AuthorSaverInterface
from domain.entities import AuthorDomain
from infrastructure.models.poems import Author


class AuthorGateway(AllAuthorReaderInterface, AuthorReaderInterface, AuthorSaverInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    @override
    async def get_authors(self) -> list[AuthorDTO] | None:

        stmt = select(Author)
        result = await self._session.execute(stmt)
        row = result.scalars()
        if row:
            convert_author_to_dto = get_converter(Iterable[Author], list[AuthorDTO])
            return convert_author_to_dto(row)
        return None

    @override
    async def read_by_uuid(self, uuid: UUID) -> AuthorDTO | None:
        stmt = select(Author).where(Author.uuid == uuid)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row:
            convert_author_to_dto = get_converter(Author, AuthorDTO)
            return convert_author_to_dto(row)
        return None

    @override
    async def save(self, author: AuthorDomain) -> None | int:
        stmt = insert(Author).values(
            uuid=author.uuid,
            fio=author.fio,
            url=author.url,
        )
        result = await self._session.execute(stmt)
        return result.returns_rows
