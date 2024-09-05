from collections.abc import Callable
from dataclasses import dataclass, field
from os import environ
from typing import Any
from urllib.parse import SplitResult


def from_env(key: str, astype: type[Any] = str) -> Callable[[], Any]:
    return lambda: astype(environ.get(key))


@dataclass
class PostgresConfig:
    host: str = field(default_factory=from_env("POSTGRES_HOST"))
    port: int = field(default_factory=from_env("POSTGRES_PORT", int))
    username: str = field(default_factory=from_env("POSTGRES_USER"))
    password: str = field(default_factory=from_env("POSTGRES_PASSWORD"))
    database: str = field(default_factory=from_env("POSTGRES_DB"))

    @property
    def uri(self) -> str:
        netloc = f"{self.username}:{self.password}@{self.host}:{self.port}"
        return SplitResult(
            "postgresql+psycopg",
            netloc=netloc,
            path=self.database,
            query="",
            fragment="",
        ).geturl()


@dataclass(slots=True)
class AppConfig:
    postgres: PostgresConfig = field(default_factory=PostgresConfig)
