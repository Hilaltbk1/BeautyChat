from uuid import uuid4
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from app.data.processed.preprocessing import preprocessing

def initialize_vectorstore():
    path=os.DATA
    belgeler=preprocessing(path )

    if not belgeler:
        print("Dökümanlar oluşturulamadı.")


    persist_directory = ("vector_store_db")
    embeddings=HuggingFaceEmbeddings(
        model_name="ytu-ce-cosmos/turkish-e5-large",
        model_kwargs={"device":"cuda"}
    )
    vector_store = None
    if not os.path.exists(persist_directory):
        print("Veritabanı bulunamadı. Yeni bir tane oluşturuluyor...")

        vector_store=Chroma.from_documents(
            documents=belgeler,
            collection_name="myVectors",
            embedding=embeddings,
            persist_directory=persist_directory
        )
        print("Veritabanı başarıyla oluşturuldu ve belgeler eklendi")
    else:
        print("Mevcut  veritabanı bulundu ,yükleniyor")
        vector_store=Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name="myVectors"
        )

    return vector_store

initialize_vectorstore()
