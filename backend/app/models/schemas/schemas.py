from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

q_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Soruyu ,bağlama göre yeniden ifade ederek tek başına anlaşılır olacak şekilde olmasını sağla."
     "Dönüşü 200 karakterı geçmesın."), #.jınja format.
    MessagesPlaceholder("chat_history"),
    ("human","{input}"),
])
qa_prompt=ChatPromptTemplate.from_messages([
    ("system","Soruyu dökümana göre cevapla :{context}"),
    MessagesPlaceholder("chat_history"),
    ("human","{input}"),
])