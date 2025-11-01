import json
import logging
from fastapi import HTTPException
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

from app.config.db import SessionLocal
from app.models.model import SessionModel, MessageModel, LogModel
from app.services.retrival_chain import retrieval_chain
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
app=FastAPI()
router=APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rag_chain =retrieval_chain()

if not rag_chain:
    raise RuntimeError('Raw_Chain is None')

class QueryRequest(BaseModel):
    query:str
    user_name:str #reacttan kullanıcı kimliği

@router.post("/search")
async def create_routers(request:QueryRequest):
    start_time = datetime.now()
    query=request.query
    user_name=request.user_name

    logger.info(f"Received query from user {user_name}:{query}")

    db_session=SessionLocal()
    human_message_entry = None
    try:
        #SessionModel tablosunda sorgu ,
        session=db_session.query(SessionModel).filter(SessionModel.user_name == user_name).first()
        if not session:
            logger.info(f"Creating new session for user{user_name}")
            #session tablosuna eklenecek python nesnesi
            session=SessionModel(user_name=user_name)
            db_session.add(session)
            db_session.commit()
            db_session.refresh(session)

        #tüm mesaj geçmişini çek o kullanıcıya ait(id)
        db_messages=db_session.query(MessageModel).filter(MessageModel.session_id == session.id).order_by(MessageModel.created_at).all()
        chat_history=[]

        for msg in db_messages:
            if msg.sender_type == "human":
                chat_history.append(HumanMessage(content=msg.content))
            elif msg.sender_type == "ai":
                chat_history.append(AIMessage(content=msg.content))

        human_message_entry=MessageModel(
            session_id=session.id,
            sender_type="human",
            content=query
        )
        db_session.add(human_message_entry)
        db_session.commit()
        db_session.refresh(human_message_entry)

        logger.info(f"Invoking RAG chain for session {session.id}...")

        response=rag_chain.invoke({"input":query,"chat_history":chat_history})
        answer=response.get("answer","No answer avaible")

        ai_message_entry=MessageModel(
            session_id=session.id,
            sender_type="ai",
            content=answer
        )
        db_session.add(ai_message_entry)
        db_session.commit()
        db_session.refresh(ai_message_entry)


        duration=(datetime.now()-start_time).total_seconds()
        success_log=LogModel(
            status_code=200,
            requests=json.dumps({"query":query}),
            response=json.dumps({"answer":answer}),
            error_message=None,
            message_id=ai_message_entry.id
        )
        db_session.add(success_log)
        db_session.commit()

        return {"query":query,"answer":answer}

    except Exception as e:
        logger.error(f"Error during query for user {user_name}: {e}")

        # Hata logunu kaydetmeye çalış
        if human_message_entry:  # Eğer 5. adımda insan mesajı kaydedilebildiyse
            error_log = LogModel(
                status_code=500,  # 500 (Sunucu Hatası)
                requests=json.dumps({"query": query}),
                response=None,  # Cevap üretemedik
                error_message=str(e),  # Hata mesajını kaydet
                message_id=human_message_entry.id  # BU ÇOK ÖNEMLİ: Logu İNSANIN SORUSUNA bağlar.
            )
            db_session.add(error_log)
            db_session.commit()

        # Hata oluştuğu için API'ye 500 hatası döndür.
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db_session.close()

@router.get("/")
async def root():
    return{"message":"WELCOME TO MY BEAUTYCHAT"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)