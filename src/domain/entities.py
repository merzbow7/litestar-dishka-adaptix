from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PoemDomain:
    uuid: UUID
    author_uuid: UUID
    author: "AuthorDomain"
    text: str
    url: str


@dataclass(frozen=True, slots=True)
class AuthorDomain:
    uuid: UUID
    fio: str
    url: str
    poems: list["PoemDomain"] | None = field(default_factory=list)
