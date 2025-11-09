from fastapi import FastAPI

from backend.router import router
from backend.lifespan import lifespan
from backend.handlers import exception_handlers
from backend.middleware import init_middleware

def get_app() -> FastAPI:

    app = FastAPI(
        title="Todo App",
        description="One page todo app on fastapi + react",
        version="1.0.0",
        lifespan=lifespan,
        exception_handlers=exception_handlers,
        redirect_slashes=False
    )
    app.include_router(router)

    init_middleware(app)

    return app
