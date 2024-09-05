from dataclasses import dataclass
from typing import final


@final
@dataclass(slots=True, frozen=True)
class NewPoemDTO:
    uuid: str
    author_uuid: str
    text: str
    url: str


@final
@dataclass(slots=True, frozen=True)
class PoemDTO:
    uuid: str
    text: str
    url: str


@final
@dataclass(slots=True, frozen=True)
class AuthorDTO:
    uuid: str
    url: str
    fio: str
