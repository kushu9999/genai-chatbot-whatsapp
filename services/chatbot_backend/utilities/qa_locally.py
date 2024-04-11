import os
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain

load_dotenv()

GROQ_API_ENDPOINT = os.getenv('GROQ_API_ENDPOINT')
GROQ_MODEL = os.getenv('GROQ_MODEL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# vectorstore location
vectorstore_path = "./models/whatsapp-rag-chatbot-models/faiss_index"

# load vectorstore from local
embedding = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

vector_store = FAISS.load_local(vectorstore_path, embedding, allow_dangerous_deserialization=True)

# getting llm
llm = ChatOpenAI(base_url=GROQ_API_ENDPOINT, model=GROQ_MODEL, api_key=GROQ_API_KEY)

# Create a question answering system based on information retrieval using the RetrievalQA class, which takes as input a neural language model, a chain type and a retriever (an object that allows you to retrieve the most relevant chunks of text for a query)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever(search_kwargs={"k": 4}))

# memory = ConversationBufferMemory(
#     memory_key='chat_history', return_messages=True)

# qa = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     retriever=vector_store.as_retriever(search_kwargs={"k": 4}),
#     memory=memory
# )


if __name__ == "__main__":
    while True:
        query = input("Please enter your question: ")
        if query.lower() == "bye":
            break

        else:
            query = f"You are restaurant assistant chatbot called RestroAI made for Restro Cafe. Your work is to solve user's query, if you don't find relevant context, respond with your knowledge Always respond within 20 words. User's question: {query}"
            result = qa.invoke(query)['result']
            print("Answer:", result)
