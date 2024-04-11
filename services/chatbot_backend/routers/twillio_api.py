import os
from utilities.twillio_utilities import send_reply
from fastapi import APIRouter, Form, Request
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv('GROQ_API_ENDPOINT')
GROQ_MODEL = os.getenv('GROQ_MODEL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


router = APIRouter()


@router.post("/twilio")
async def twilio(request: Request, Body: str = Form(...), From: str = Form(...)):
    try:
        query = Body
        sender_id = From
        print(sender_id, query)


        # vectorstore location
        vectorstore_path = "./models/whatsapp-rag-chatbot-models/faiss_index"

        # load vectorstore from local
        embedding = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

        vector_store = FAISS.load_local(vectorstore_path, embedding, allow_dangerous_deserialization=True)

        # getting llm
        llm = ChatOpenAI(base_url=GROQ_API_ENDPOINT, model=GROQ_MODEL, api_key=GROQ_API_KEY)

        # Create a question answering system based on information retrieval using the RetrievalQA class, which takes as input a neural language model, a chain type and a retriever (an object that allows you to retrieve the most relevant chunks of text for a query)
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever(search_kwargs={"k": 4}))

        # retrive results from llm
        query = f"You are restaurant assistant chatbot called RestroAI made for Restro Cafe. Your work is to solve user's query and maintain healthy conversations, if you don't find relevant context, respond with your knowledge Always respond within 20 words. Only respond answer nothing extra information. User's question: {query}"
        result = qa.invoke(query)['result']

        print(result)

        # reply back to user
        send_reply(sender_id, result)

    except Exception as e:
        result = f"Something went wrong. Error: {e}"
        send_reply(sender_id, result)

    return {"message": "Message sent sucessfully"}
