import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    Docx2txtLoader
)

SUPPORTED_FILES = (".pdf", ".csv", ".docx", ".txt")


def load_documents(folder_path: str):
    """
    Load all supported documents from a folder.
    """

    documents = []

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"{folder_path} folder not found.")

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        if not filename.lower().endswith(SUPPORTED_FILES):
            print(f"Skipping: {filename}")
            continue

        try:

            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)

            elif filename.endswith(".csv"):
                loader = CSVLoader(file_path)

            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)

            elif filename.endswith(".txt"):
                loader = TextLoader(file_path)

            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = filename

            documents.extend(docs)

            print(f"Loaded: {filename}")

        except Exception as e:
            print(f"Error loading {filename}")
            print(e)

    return documents