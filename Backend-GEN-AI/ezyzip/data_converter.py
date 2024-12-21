from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

def load_pdf(file_path):
    loader = PyPDFLoader(file_path) 
    documents = loader.load()
    return documents

def convert_data(file_path):
    extracted_documents = load_pdf(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    text_chunks = splitter.split_documents(extracted_documents)
    return text_chunks

if __name__ == "__main__":
    file_path = r"C:\Users\aashutosh kumar\Downloads\MB1.pdf"
    text_chunks = convert_data(file_path)
    print(len(text_chunks), "\n")
    print(text_chunks[:5])
