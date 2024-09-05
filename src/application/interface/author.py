from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from application.dto import AuthorDTO
from domain.entities import AuthorDomain, PoemDomain


class AuthorSaverInterface(Protocol):
    @abstractmethod
    async def save(self, author: AuthorDomain) -> int | None:
        pass


class AllAuthorReaderInterface(Protocol):
    @abstractmethod
    async def get_authors(self) -> list[AuthorDTO] | None:
        pass


class AuthorReaderInterface(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: UUID) -> AuthorDTO | None:
        pass
