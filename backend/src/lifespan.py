from contextlib import asynccontextmanager

@asynccontextmanager
def lifespan(app, **kwargs):
    yield