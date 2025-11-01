from fastapi import FastAPI
from app.config.middleware import create_middleware
from app.routes  import  search
from app.routes.history import router as historyRouter


def create_app() -> FastAPI:
    app = FastAPI()

    create_routers(app)
    create_middleware(app)
    return app

def create_routers(app:FastAPI):
    app.include_router(search.router)
    app.include_router(historyRouter)

app =create_app()