import uvicorn
from backend.app.services.retrival_chain import retrieval_chain
from fastapi import FastAPI, APIRouter
from session import search

app=FastAPI()
router=APIRouter()
rag_chain =retrieval_chain()

if not rag_chain:
    raise RuntimeError('Raw_Chain is None')

@router.post("/search")
async def create_routers():

    searching=search()
    return searching

@router.get("/")
async def root():
    return{"message":"WELCOME TO MY BEAUTYCHAT"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)