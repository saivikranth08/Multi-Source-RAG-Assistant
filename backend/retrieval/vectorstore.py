from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from backend.utils.config import COLLECTION_NAME
from backend.utils.logger import logger
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

def get_qdrant_client():
    """Use in-memory Qdrant to avoid concurrent access issues with local path mode"""
    return QdrantClient(":memory:")

def clear_collection():
    client = get_qdrant_client()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        try:
            client.delete_collection(COLLECTION_NAME)
            logger.info(f"Deleted collection '{COLLECTION_NAME}'")
        except Exception as e:
            logger.warning(f"Could not delete collection: {e}")
    
    try:
        # Create collection with minimal parameters to avoid Pydantic validation issues
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        logger.info(f"Created collection '{COLLECTION_NAME}'")
    except Exception as e:
        # If create_collection fails due to Pydantic, try with recreate_collection
        logger.warning(f"create_collection failed: {e}. Trying recreate_collection...")
        try:
            client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            logger.info(f"Created collection '{COLLECTION_NAME}' using recreate_collection")
        except Exception as e2:
            logger.error(f"Both methods failed: {e2}")
            raise

def create_vectorstore(chunks, embedding_model):
    client = get_qdrant_client()
    existing = [c.name for c in client.get_collections().collections]
    
    if COLLECTION_NAME not in existing:
        try:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except Exception as e:
            logger.warning(f"create_collection failed: {e}. Trying recreate_collection...")
            try:
                client.recreate_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
            except Exception as e2:
                logger.error(f"Both methods failed: {e2}")
                raise
    
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embedding_model
    )
    vectorstore.add_documents(chunks)
    logger.info(f"Added {len(chunks)} chunks to vectorstore")
    return vectorstore

def load_vectorstore(embedding_model):
    client = get_qdrant_client()
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embedding_model
    )

def create_hybrid_retriever(vectorstore, chunks, k=10):
    # Dense retriever — Qdrant semantic search
    dense_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": k * 3}
    )

    # Sparse retriever — BM25 keyword search
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = k

    # Combine both
    hybrid_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, bm25_retriever],
        weights=[0.6, 0.4]
    )

    return hybrid_retriever


import cohere
import os


def rerank_results(query, documents, top_n=3):
    """Rerank documents using Cohere's rerank API"""
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    # Extract text from documents
    texts = [doc.page_content for doc in documents]
    # Rerank
    response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=texts,
        top_n=top_n
    )
    # Return reranked documents in order
    reranked_docs = [documents[result.index] for result in response.results]
    return reranked_docs