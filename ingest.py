from loaders import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

UPLOAD_FOLDER = "uploads"
VECTOR_DB = "vector_db"


def build_vector_database():
    print("📂 Loading documents...")

    documents = load_documents(UPLOAD_FOLDER)

    if len(documents) == 0:
        print("❌ No documents found!")
        return False

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"✅ Chunks Created: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(chunks, embeddings)

    if os.path.exists(VECTOR_DB):
        import shutil
        shutil.rmtree(VECTOR_DB)

    db.save_local(VECTOR_DB)

    print("✅ Vector Database Created!")

    return True


if __name__ == "__main__":
    build_vector_database()