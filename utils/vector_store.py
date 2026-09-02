# import uuid
# import os
# import numpy as np
# import chromadb
# from typing import List
# import hashlib
# from langchain_core.documents import Document

# class VectorStore:
#     def __init__(self, db_name="pro"):
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#         self.collection_name = f"{db_name}_db"

#         self.persist_directory = os.path.join(
#             BASE_DIR,
#             "vector_db",
#             self.collection_name
#         )
    
#         os.makedirs(self.persist_directory, exist_ok=True)

#         self.client = chromadb.PersistentClient(
#             path=self.persist_directory
#         )

#         self.collection = self.client.get_or_create_collection(
#             name=self.collection_name
#         )

#     def generate_chunk_hash(self, chunk):
#         """
#         Generate SHA-256 hash for a chunk.
#         """
#         return hashlib.sha256(chunk.encode("utf-8")).hexdigest()

#     def chunk_exists(self, chunk_hash):
#         """
#         Check if a chunk with this hash already exists.
#         """

#         result = self.collection.get(where={"chunk_hash": chunk_hash})

#         return len(result["ids"]) > 0

#     def add_documents(self, chunks: List[Document], embeddings: np.ndarray):
#         """
#         Store chunks and their embeddings inside ChromaDB.

#         Args:
#             chunks: List of LangChain Document objects.
#             embeddings: NumPy array of embeddings.
#         """

#         if len(chunks) != len(embeddings):
#             raise ValueError("Number of chunks must match number of embeddings.")

#         ids = []
#         texts = []
#         vectors = []
#         metadatas = []

#         for i, (doc, embedding) in enumerate(zip(chunks, embeddings)):

#             # ids.append(f"chunk_{i}")
#             ids.append(str(uuid.uuid4()))

#             texts.append(doc.page_content)

#             vectors.append(embedding.tolist())

#             metadatas.append(dict(doc.metadata))

#         try:
#             self.collection.add(
#                 ids=ids,
#                 documents=texts,
#                 embeddings=vectors,
#                 metadatas=metadatas
#             )

#             print("Documents added successfully!")

#         except Exception as e:
#             print(e)


#     def get_document_count(self):
#         """Return the number of stored chunks."""
#         return self.collection.count()

#     def show_documents(self, n=5):
#         """
#         Display the first few stored chunks.
#         """
#         data = self.collection.get(limit=n)

#         print("\nStored Documents\n")

#         for i in range(len(data["ids"])):

#             print(f"ID: {data['ids'][i]}")

#             print(f"Metadata: {data['metadatas'][i]}")

#             print(f"Text: {data['documents'][i][:150]}...")

#             print("-" * 60)

#     def clear_collection(self):
#         """
#         Delete all chunks from the collection.
#         Useful while developing/testing.
#         """

#         all_ids = self.collection.get()["ids"]

#         if all_ids:
#             self.collection.delete(ids=all_ids)

# if __name__ == "__main__":
#     print("Pro docs")
#     temp = VectorStore("pro")
#     # print("HHHHHH", temp.get_document_count())
#     # temp.clear_collection()
#     temp.show_documents(n=50)
#     print(temp.get_document_count())
    

#     print("Con docs")
#     temp = VectorStore("con")
#     # print("HHHHHH", temp.get_document_count())
#     # temp.clear_collection()
#     temp.show_documents(n=50)
#     print(temp.get_document_count())


import uuid
import os
import numpy as np
import chromadb
from typing import List
import hashlib
from langchain_core.documents import Document


class VectorStore:

    def __init__(self, db_name="pro"):

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.collection_name = f"{db_name}_db"

        self.persist_directory = os.path.join(
            BASE_DIR,
            "vector_db",
            self.collection_name
        )

        os.makedirs(
            self.persist_directory,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )


    def generate_chunk_hash(self, chunk):

        return hashlib.sha256(
            chunk.encode("utf-8")
        ).hexdigest()


    def chunk_exists(self, chunk_hash):

        result = self.collection.get(
            where={
                "chunk_hash": chunk_hash
            }
        )

        return len(result["ids"]) > 0


    def add_documents(
        self,
        chunks: List[Document],
        embeddings: np.ndarray
    ):

        if len(chunks) != len(embeddings):

            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        ids = []
        texts = []
        vectors = []
        metadatas = []

        for doc, embedding in zip(
            chunks,
            embeddings
        ):

            ids.append(
                str(uuid.uuid4())
            )

            texts.append(
                doc.page_content
            )

            vectors.append(
                embedding.tolist()
            )

            metadatas.append(
                dict(doc.metadata)
            )

        try:

            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=vectors,
                metadatas=metadatas
            )

            print(
                "Documents added successfully!"
            )

        except Exception as e:

            print(e)


    def get_document_count(self):

        return self.collection.count()


    def show_documents(self, n=5):

        data = self.collection.get(
            limit=n
        )

        print("\nStored Documents\n")

        for i in range(
            len(data["ids"])
        ):

            print(
                f"ID: {data['ids'][i]}"
            )

            print(
                f"Metadata: {data['metadatas'][i]}"
            )

            print(
                f"Text: {data['documents'][i][:150]}..."
            )

            print(
                "-" * 60
            )


    def clear_collection(self):

        all_ids = self.collection.get()["ids"]

        deleted_count = len(all_ids)

        if all_ids:

            self.collection.delete(
                ids=all_ids
            )

        return deleted_count


if __name__ == "__main__":

    print("Pro docs")

    temp = VectorStore("pro")

    temp.show_documents(n=50)

    print(temp.get_document_count())

    print("Con docs")

    temp = VectorStore("con")

    temp.show_documents(n=50)

    print(temp.get_document_count())

