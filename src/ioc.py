from collections.abc import AsyncIterable
from uuid import uuid4

from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application import interface
from application.interactor.author import GetAllAuthorsInteractor, GetAuthorInteractor, NewAuthorInteractor
from config import AppConfig
from infrastructure.database import new_session_maker
from infrastructure.gateway.author import AuthorGateway


class AppProvider(Provider):
    config = from_context(provides=AppConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interface.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: AppConfig) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, interface.DBSession]]:
        async with session_maker() as session:
            yield session

    author_gateway = provide(
        AuthorGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interface.AuthorReaderInterface,
            interface.AllAuthorReaderInterface,
            interface.AuthorSaverInterface
        ]
    )

    get_author_interactor = provide(GetAuthorInteractor, scope=Scope.REQUEST)
    get_all_authors_interactor = provide(GetAllAuthorsInteractor, scope=Scope.REQUEST)
    create_new_author_interactor = provide(NewAuthorInteractor, scope=Scope.REQUEST)
