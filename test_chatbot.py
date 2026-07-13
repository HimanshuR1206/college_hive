from chatbot import ask_question

print("=" * 50)
print("🎓 Welcome to CollegeHive AI")
print("Type 'exit' to quit")
print("=" * 50)

while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    answer, docs = ask_question(question)

    print("\nBot:")
    print(answer)

    print("\nSources:")
    for doc in docs:
        print("-", doc.metadata.get("source", "Unknown"))