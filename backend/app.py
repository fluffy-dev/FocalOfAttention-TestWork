from fastapi import FastAPI

from backend.router import router
from backend.lifespan import lifespan
from backend.handlers import exception_handlers

def get_app() -> FastAPI:

    app = FastAPI(
        title="Todo App",
        description="One page todo app on fastapi + react",
        version="1.0.0",
        lifespan=lifespan,
        exception_handlers=exception_handlers,
    )
    app.include_router(router)

    #TODO add logging setup and cors init
    return app