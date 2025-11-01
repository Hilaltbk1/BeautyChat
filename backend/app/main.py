from fastapi import FastAPI
from app.routers.search import routers
from wsgi import create_middleware
from app.wsgi import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)