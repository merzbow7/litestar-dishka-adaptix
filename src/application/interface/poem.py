from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from application.dto import PoemDTO


class PoemSaver(Protocol):
    @abstractmethod
    async def save(self, author: PoemDTO) -> None:
        pass


class PoemReaderInterface(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: UUID) -> PoemDTO | None:
        pass


class AuthorPoemReader(Protocol):
    @abstractmethod
    async def read_by_author_uuid(self, uuid: UUID) -> PoemDTO | None:
        pass
