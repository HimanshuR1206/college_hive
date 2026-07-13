from dotenv import load_dotenv
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# Load .env file
load_dotenv()

# Read API Key
groq_api_key = os.getenv("GROQ_API_KEY")

print("API KEY:", groq_api_key)

if groq_api_key is None or groq_api_key.strip() == "":
    raise ValueError("❌ GROQ_API_KEY not found.")

# Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS Vector Database
db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# Create Retriever
retriever = db.as_retriever(
    search_kwargs={"k": 5}
)

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Ask Question Function
def ask_question(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are CollegeHive AI.

Answer ONLY from the provided context.

If the answer is not available, reply:
'I couldn't find that information in the uploaded documents.'

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content, docs