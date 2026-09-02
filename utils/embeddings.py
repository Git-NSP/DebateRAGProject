# from typing import List
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from langchain_core.documents import Document

# class EmbeddingManager:
#     """
#     Generates embeddings for LangChain Document chunks using
#     SentenceTransformer.
#     """

#     def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
#         self.model_name = model_name
#         self.model = SentenceTransformer(model_name)

#     def generate_embeddings(self, chunks: List[Document]) -> np.ndarray:
#         """
#         Generate embeddings for a list of LangChain Document chunks.

#         Args:
#             chunks: List of LangChain Document objects.

#         Returns:
#             NumPy array of embeddings.
#         """

#         if not chunks:
#             raise ValueError("No chunks provided for embedding generation.")

#         # Extract only the text from each chunk
#         texts = [chunk.page_content for chunk in chunks]

#         embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

#         return embeddings

#     def get_embedding_dimension(self) -> int:
#         """Return the embedding dimension of the model."""
#         return self.model.get_embedding_dimension()
    

# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------



import os
import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_core.documents import Document
from typing import List

class EmbeddingManager:

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):

        load_dotenv()

        self.model_name = model_name

        hf_token = os.getenv("HF_TOKEN")

        if not hf_token:
            raise ValueError(
                "HF_TOKEN environment variable is missing."
            )

        self.client = InferenceClient(
            provider="hf-inference",
            api_key=hf_token
        )


    def generate_embeddings(self, chunks: List[Document]) -> np.ndarray:

        if not chunks:
            raise ValueError(
                "No chunks provided for embedding generation."
            )

        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.client.feature_extraction(
            texts,
            model=self.model_name,
            normalize=True
        )

        return np.array(
            embeddings,
            dtype=np.float32
        )


    def generate_query_embedding(self, query: str) -> List[float]:

        embedding = self.client.feature_extraction(
            query,
            model=self.model_name,
            normalize=True
        )

        return np.array(
            embedding,
            dtype=np.float32
        ).tolist()


    def get_embedding_dimension(self):
        return 384
