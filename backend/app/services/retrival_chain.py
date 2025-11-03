from backend.app.config import config
from .vector_store import initialize_vectorstore
from ..prompt.prompt import qa_prompt, q_prompt
from ..config.config import settings
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def retrieval_chain():
    db=initialize_vectorstore()
    retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    if not config.settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set")

    llm=ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        max_tokens=2048
    )
    history_aware_retriever= create_history_aware_retriever(llm,retriever,q_prompt)
    document_chain=create_stuff_documents_chain(
        llm=llm,
        prompt=qa_prompt
    )

    return create_retrieval_chain(history_aware_retriever,document_chain)