from utils.retriever import Retriever

retriever = Retriever("pro")

docs = retriever.retrieve("What does the certificate say?", top_k=3)

print()

for i, doc in enumerate(docs):

    print("=" * 60)

    print(i + 1)

    print()

    print(doc.page_content[:500])

    # print()

    # # print(doc.metadata)


