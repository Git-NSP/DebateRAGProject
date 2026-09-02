# from typing import List
# from langchain_core.documents import Document

# from utils.vector_store import VectorStore
# from utils.embeddings import EmbeddingManager


# class Retriever:

#     def __init__(self, side: str):

#         self.side = side

#         self.vector_db = VectorStore(side)

#         self.embedding_model = EmbeddingManager()

#     def retrieve(
#         self,
#         query: str,
#         top_k: int = 5
#     ) -> List[Document]:

#         query_embedding = self.embedding_model.model.encode(
#             query
#         ).tolist()

#         results = self.vector_db.collection.query(
#             query_embeddings=[query_embedding],
#             n_results=top_k
#         )

#         documents = []

#         if not results["documents"]:
#             return documents

#         retrieved_documents = results["documents"][0]
#         retrieved_metadatas = results["metadatas"][0]

#         for index, (text, metadata) in enumerate(
#             zip(
#                 retrieved_documents,
#                 retrieved_metadatas
#             ),
#             start=1
#         ):

#             metadata = dict(metadata)

#             metadata["retrieval_id"] = f"DOC {index}"

#             documents.append(
#                 Document(
#                     page_content=text,
#                     metadata=metadata
#                 )
#             )

#         return documents



from typing import List
from langchain_core.documents import Document
from utils.vector_store import VectorStore
from utils.embeddings import EmbeddingManager

class Retriever:

    def __init__(self,side: str):

        self.side = side

        self.vector_db = VectorStore(
            side
        )

        self.embedding_model = (
            EmbeddingManager()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Document]:

        query_embedding = (
            self.embedding_model.model.encode(
                query
            ).tolist()
        )

        results = (
            self.vector_db.collection.query(
                query_embeddings=[
                    query_embedding
                ],
                n_results=top_k
            )
        )

        documents = []

        if not results[
            "documents"
        ]:

            return documents

        retrieved_documents = (
            results["documents"][0]
        )

        retrieved_metadatas = (
            results["metadatas"][0]
        )

        for index, (
            text,
            metadata
        ) in enumerate(
            zip(
                retrieved_documents,
                retrieved_metadatas
            ),
            start=1
        ):

            metadata = dict(
                metadata
            )

            metadata[
                "retrieval_id"
            ] = f"DOC {index}"

            documents.append(
                Document(
                    page_content=text,
                    metadata=metadata
                )
            )

        return documents


