import json
import numpy as np

from logger import logger
from sentence_transformers import SentenceTransformer

from config import KNOWLEDGE_BASE_FILE, EMBEDDING_MODEL, TOP_K


MODEL_NAME = EMBEDDING_MODEL


def load_knowledge_base():
    logger.info(
        f"Loading knowledge base: {KNOWLEDGE_BASE_FILE}"
    )

    with open(
        KNOWLEDGE_BASE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        knowledge_base = json.load(file)

    logger.info(
        f"Knowledge base loaded: {len(knowledge_base)} chunks"
    )

    return knowledge_base


def load_embedding_model():
    """
    Load the embedding model.
    """
    logger.info(
        f"Loading embedding model: {MODEL_NAME}"
    )

    model = SentenceTransformer(MODEL_NAME)

    logger.info(
        "Embedding model loaded successfully"
    )

    return model


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """
    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )


def search_chunks(
    query: str,
    knowledge_base: list[dict],
    model,
    top_k: int = TOP_K
) -> list[dict]:
    """
    Find the most relevant chunks from the saved knowledge base.
    """

    logger.info(
        f"Running semantic search for query: {query}"
    )

    query_embedding = model.encode(query).tolist()

    results = []

    for chunk in knowledge_base:

        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    logger.info(
        f"Retrieved top {top_k} relevant chunks"
    )

    return results[:top_k]


if __name__ == "__main__":

    print("=" * 70)
    print("SAVED KNOWLEDGE BASE SEARCH TEST")
    print("=" * 70)

    print("\nLoading knowledge base...")

    knowledge_base = load_knowledge_base()

    print(
        f"Knowledge base loaded: "
        f"{len(knowledge_base)} chunks"
    )

    model = load_embedding_model()

    query = "When must the vendor report a data security incident?"

    results = search_chunks(
        query,
        knowledge_base,
        model,
        top_k=3
    )

    print("\nQuery:")
    print(query)

    print("\nTop relevant chunks:")

    for rank, result in enumerate(results, start=1):

        print("\n" + "-" * 70)

        print(f"Rank       : {rank}")
        print(f"Chunk ID    : {result['chunk_id']}")
        print(f"Page       : {result['page']}")
        print(f"Similarity : {result['score']:.4f}")

        print("\nText:")
        print(result["text"])

    print("\n" + "=" * 70)
    print("SAVED KNOWLEDGE BASE SEARCH SUCCESSFUL!")
    print("=" * 70)