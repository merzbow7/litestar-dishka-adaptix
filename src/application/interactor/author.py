from uuid import UUID

from application import interface
from application.dto import AuthorDTO
from domain import entities


class GetAllAuthorsInteractor:
    def __init__(
            self,
            author_gateway: interface.AllAuthorReaderInterface,
    ) -> None:
        self._author_gateway = author_gateway

    async def __call__(self) -> list[AuthorDTO] | None:
        return await self._author_gateway.get_authors()


class GetAuthorInteractor:
    def __init__(
            self,
            author_gateway: interface.AuthorReaderInterface,
    ) -> None:
        self._author_gateway = author_gateway

    async def __call__(self, uuid: UUID) -> AuthorDTO | None:
        return await self._author_gateway.read_by_uuid(uuid)


class NewAuthorInteractor:
    def __init__(
            self,
            db_session: interface.DBSession,
            book_gateway: interface.AuthorSaverInterface,
            uuid_generator: interface.UUIDGenerator,
    ) -> None:
        self._db_session = db_session
        self._book_gateway = book_gateway
        self._uuid_generator = uuid_generator

    async def __call__(self, dto: AuthorDTO) -> UUID:
        uuid = self._uuid_generator()
        book = entities.AuthorDomain(
            uuid=uuid,
            fio=dto.fio,
            url=dto.url
        )

        await self._book_gateway.save(book)
        await self._db_session.commit()
        return uuid
