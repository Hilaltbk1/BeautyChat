from fastapi import FastAPI
from app.routes.search import router
from app.config.middleware import create_middleware
from app.wsgi import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)