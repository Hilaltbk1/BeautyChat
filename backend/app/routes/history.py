from fastapi import FastAPI, HTTPException, APIRouter
from app.models.model  import SessionModel,LogModel,MessageModel
from app.config.db import SessionLocal

import json
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/history/{user_name}")
async def get_history(user_name: str, limit:int =10):
    #sql alchemy ile vt bağlan
    db_session = SessionLocal()
    try:
        #kullanıcının sessıonı çekme
        session = db_session.query(SessionModel)\
            .filter(SessionModel.user_name == user_name).first()
        if not session:
            logger.info(f"Didn't find session for user {user_name}")
            return {"history": []}

        db_messages = db_session.query(MessageModel)\
            .filter(MessageModel.session_id == session.id)\
            .order_by(MessageModel.created_at)\
            .limit(limit)\
            .all()

        chat_history = []
        for message in db_messages:
            chat_history.append({
                "id": message.id,
                "sender": message.sender_type,
                "content": message.content,
                "created_at": message.created_at.isoformat()
            })

        return {"history": chat_history}

    except Exception as e:
        logger.error(f"Error fetching history for user {user_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db_session.close()
