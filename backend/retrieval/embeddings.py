# from langchain_huggingface import HuggingFaceEmbeddings
# from backend.utils.config import EMBEDDING_MODEL

# def load_embeddings():
#     model = HuggingFaceEmbeddings(
#         model_name="all-MiniLM-L6-v2",
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"normalize_embeddings": True, "batch_size": 32}
#     )
#     return model

from langchain_huggingface import HuggingFaceEmbeddings
from backend.utils.config import EMBEDDING_MODEL

def load_embeddings():
    model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32}
    )
    return model