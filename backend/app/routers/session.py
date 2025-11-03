import json
from pydantic import BaseModel
from  backend.app.config.db import SessionLocal
from backend.app.models.model import SessionModel, MessageModel, LogModel
import logging
from fastapi import  HTTPException
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

from backend.app.routers.search import rag_chain

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)


def getHistory(user_name:str,limit:int =10):
    db_session = SessionLocal()

    try:
        #kullanıcı sessionu çekme
        session=db_session.query(SessionModel)\
        .filter(SessionModel.user_name == user_name).first()
        if not session:
            logger.info(f"Didn't find session for user {user_name}")
            return []

        #message id
        db_messages=db_session.query(MessageModel)\
        .filter(MessageModel.session_id == session.id)\
        .order_by(MessageModel.created_at.desc())\
        .limit(limit) .all()

        return db_messages

    except Exception as e:
        logger.info(f"Didn't find session for user {user_name} : {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_session.close()


class QueryRequest(BaseModel):
    query: str
    user_name: str


def search(request:QueryRequest):
    start_time=datetime.now()
    query=request.query
    user_name=request.user_name

    logger.info(f"Received query from user {user_name}:{query}")
    db_session=SessionLocal()
    human_message_entry=None
    try:
        #Sessionmodel tablosunda sorgu
        session=db_session.query(SessionModel).filter(SessionModel.user_name == user_name).first()
        if not session:
            logger.info(f"Creating new session for user {user_name}")
            #session tablosuna eklenecek
            session=SessionModel(user_name=user_name)
            db_session.add(session)
            db_session.commit()
            db_session.refresh(session)

        #O kullanıcıya ait(id'li) tüm mesaj geçmişini filtrele
        db_messages=db_session.query(MessageModel).filter(MessageModel.session_id == session.id).order_by(MessageModel.created_at).limit(20).all()
        db_messages.reverse()
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

        logger.info(f"Invoking RAG chain for session {session.id}")

        response=rag_chain.invoke({"input":query,"chat_history":chat_history})
        answer=response.get("answer","No answer avaible")

        ai_message=MessageModel(
            session_id=session.id,
            sender_type="ai",
            content=answer
        )
        db_session.add(ai_message)
        db_session.commit()
        db_session.refresh(ai_message)

        duration = (datetime.now() - start_time).total_seconds()
        succes_log = LogModel(
            status_code=200,
            request=json.dumps({"query":query}),
            response=json.dumps({"answer":answer}),
            error_message=None,
            message_id= human_message_entry.id
        )
        db_session.add(succes_log)
        db_session.commit()
        return {"query": query,"answer":answer}

    except Exception as e:
        logger.error(f"Error during query for user {user_name}: {e}")

        if human_message_entry:
            error_log=LogModel(
                status_code=500,
                request=json.dumps({"query":query}),
                response=None,
                error_message=str(e),
                message_id=human_message_entry.id
            )
            db_session.add(error_log)
            db_session.commit()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_session.close()
