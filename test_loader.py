from loaders import load_documents

documents = load_documents("uploads")

print("=" * 50)
print(f"Documents Loaded: {len(documents)}")
print("=" * 50)

if documents:
    print(documents[0].page_content[:500])
    print(documents[0].metadata)
else:
    print("No documents found.")