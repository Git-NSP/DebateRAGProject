from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

class EmbeddingManager:
    """
    Generates embeddings for LangChain Document chunks using
    SentenceTransformer.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, chunks: List[Document]) -> np.ndarray:
        """
        Generate embeddings for a list of LangChain Document chunks.

        Args:
            chunks: List of LangChain Document objects.

        Returns:
            NumPy array of embeddings.
        """

        if not chunks:
            raise ValueError("No chunks provided for embedding generation.")

        # Extract only the text from each chunk
        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

        return embeddings

    def get_embedding_dimension(self) -> int:
        """Return the embedding dimension of the model."""
        return self.model.get_embedding_dimension()
    

    
# from typing import List
# from functools import lru_cache

# import numpy as np

# from sentence_transformers import SentenceTransformer
# from langchain_core.documents import Document


# @lru_cache(maxsize=None)
# def load_embedding_model(
#     model_name: str
# ):

#     print(
#         f"Loading embedding model: {model_name}"
#     )

#     return SentenceTransformer(
#         model_name
#     )


# class EmbeddingManager:

#     def __init__(
#         self,
#         model_name: str = "BAAI/bge-small-en-v1.5"
#     ):

#         self.model_name = model_name

#         self.model = load_embedding_model(
#             model_name
#         )

#     def generate_embeddings(
#         self,
#         chunks: List[Document]
#     ) -> np.ndarray:

#         if not chunks:

#             raise ValueError(
#                 "No chunks provided for embedding generation."
#             )

#         texts = [
#             chunk.page_content
#             for chunk in chunks
#         ]

#         embeddings = self.model.encode(
#             texts,
#             show_progress_bar=True,
#             convert_to_numpy=True
#         )

#         return embeddings

#     def get_embedding_dimension(self) -> int:

#         return self.model.get_embedding_dimension()
    
