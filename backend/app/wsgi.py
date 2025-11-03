from fastapi import FastAPI
from backend.app.routers  import  search
from backend.app.routers.history import router as historyRouter
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    create_routers(app)
    create_middleware(app)
    return app

def create_routers(app:FastAPI):
    app.include_router(search.router)
    app.include_router(historyRouter)

def create_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'])


app =create_app()