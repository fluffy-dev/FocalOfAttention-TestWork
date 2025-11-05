from fastapi import FastAPI

from src.lifespan import lifespan
from src.handlers import exception_handlers

def get_app() -> FastAPI:

    app = FastAPI(
        title="Todo App",
        description="One page todo app on fastapi + react",
        version="1.0.0",
        lifespan=lifespan,
        exception_handlers=exception_handlers,
    )

    #TODO add logging setup and cors init
    return app