from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, HttpMethod, route
from litestar.exceptions import HTTPException
from litestar.params import Body

from application.dto import AuthorDTO
from application.interactor import GetAuthorInteractor
from application.interactor.author import GetAllAuthorsInteractor


class HTTPAuthorController(Controller):
    path = "/author"

    @route(http_method=HttpMethod.GET, path="/{author_id:uuid}")
    @inject
    async def get_author(
            self,
            author_id: Annotated[UUID, Body(description="Author ID", title="Author ID")],
            interactor: Depends[GetAuthorInteractor],
    ) -> AuthorDTO:
        book_domain = await interactor(uuid=author_id)
        if not book_domain:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Author not found")
        return book_domain

    @route(http_method=HttpMethod.GET)
    @inject
    async def get_authors(
            self,
            interactor: Depends[GetAllAuthorsInteractor],
    ) -> list[AuthorDTO]:
        book_domain = await interactor()
        if not book_domain:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Author not found")
        return book_domain
