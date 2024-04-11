from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# load PDF files from a directory
loader = PyPDFLoader("./data/whatsapp-rag-chatbot.pdf")
data = loader.load()
# print the loaded data, which is a list of tuples (file name, text extracted from the PDF)
print(data)

# split the extracted data into text chunks using the text_splitter, which splits the text based on the specified number of characters and overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
text_chunks = text_splitter.split_documents(data)
# print the number of chunks obtained
print(len(text_chunks))

# OpenAI Embedddings
embedding = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)

# create embeddings for each text chunk using the FAISS class, which creates a vector index using FAISS and allows efficient searches between vectors
vector_store = FAISS.from_documents(text_chunks, embedding=embedding)

# save vectorstore
vectorstore_path = "./models/whatsapp-rag-chatbot-models/faiss_index"
vector_store.save_local(vectorstore_path)
