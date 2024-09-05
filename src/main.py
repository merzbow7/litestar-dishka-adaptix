from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar

from config import AppConfig
from controllers.http.api.author import HTTPAuthorController
from ioc import AppProvider

config = AppConfig()
container = make_async_container(AppProvider(), context={AppConfig: config})


def get_litestar_app() -> Litestar:
    litestar_app = Litestar(
        route_handlers=[HTTPAuthorController],
        debug=True,
    )
    litestar_integration.setup_dishka(container, litestar_app)
    return litestar_app


def get_app() -> Litestar:
    return get_litestar_app()
