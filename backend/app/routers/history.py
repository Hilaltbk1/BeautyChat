from fastapi import FastAPI, HTTPException, APIRouter
from app.routers.session import getHistory
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/history/{user_name}")
async def get_history():
    try:
        chat_history = []
        db_messages=getHistory()
        for message in db_messages:
            chat_history.append({
                "id": message.id,
                "sender": message.sender_type,
                "content": message.content,
                "created_at": message.created_at.isoformat()
                })

        return {"history": chat_history}

    except Exception as e:
        logger.error(f"Error fetching history  {e}")
        raise HTTPException(status_code=500, detail=str(e))


