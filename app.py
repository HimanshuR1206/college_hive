import os
import shutil
import streamlit as st

from ingest import build_vector_database
from chatbot import ask_question

# ---------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="College_Hive",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 College_Hive")
st.markdown("### AI-Powered College Recommendation Chatbot")

# ---------------------------------------------------
# Chat History
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# Sidebar - Upload Documents
# ---------------------------------------------------

with st.sidebar:

    st.header("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, TXT or CSV",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True
    )

    if st.button("📚 Build Knowledge Base"):

        if uploaded_files:

            # Remove old uploads
            if os.path.exists("uploads"):
                shutil.rmtree("uploads")

            os.makedirs("uploads", exist_ok=True)

            # Save uploaded files
            for file in uploaded_files:

                with open(os.path.join("uploads", file.name), "wb") as f:
                    f.write(file.getbuffer())

            with st.spinner("Creating Vector Database..."):

                success = build_vector_database()

            if success:

                st.success("✅ Knowledge Base Created Successfully!")

            else:

                st.error("No documents found.")

        else:

            st.warning("Please upload at least one file.")

# ---------------------------------------------------
# Display Previous Messages
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------

question = st.chat_input("Ask anything about your uploaded documents...")

if question:

    # Show User Message
    st.chat_message("user").markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Generate Response
    with st.spinner("Thinking..."):

        answer, docs = ask_question(question)

    # Show Assistant Responseghg
    with st.chat_message("assistant"):

        st.markdown(answer)

        st.markdown("### 📄 Source Documents")

        shown = set()

        for doc in docs:

            source = doc.metadata.get("source", "Unknown")

            if source not in shown:

                st.write(f"✅ {source}")

                shown.add(source)

    # Save Assistant Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )