from chatbot.data_converter import convert_data
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os

def ingest_data(status):
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ASTRA_API_KEY = os.getenv("ASTRA_API_KEY")
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_ID = os.getenv("DB_ID")
    LANGCHAIN_TRACING_V2= True
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT="Medical_Summarizer"
    print(ASTRA_API_KEY)
    gemini_embedding = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    print("Gemini embedding done.")
    vector_store = AstraDBVectorStore(embedding = gemini_embedding,
                                      api_endpoint = DB_ENDPOINT,
                                      namespace = "default_keyspace",
                                      token = ASTRA_API_KEY,
                                      collection_name = "Medical")
    print("Database initialized")
    is_full = status
    if is_full == None:
        text_chunks = convert_data(r"C:\Users\aashutosh kumar\Downloads\MB1.pdf")
        print("Text Chunks are created", len(text_chunks))
        inserted_ids = vector_store.add_documents(text_chunks)
    else:
        return vector_store
    
    
    return vector_store,inserted_ids


if __name__ == "__main__":
    vector_store = ingest_data(None)
    print("DB has been initialized")