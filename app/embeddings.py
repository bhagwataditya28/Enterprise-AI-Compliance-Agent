from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL

MODEL_NAME = EMBEDDING_MODEL


def load_embedding_model():
    """
    Load the local sentence-transformer embedding model.
    """

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding model loaded successfully!")

    return model


def create_embeddings(chunks: list[dict], model) -> list[dict]:
    """
    Generate an embedding vector for each document chunk.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page": chunk["page"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    return embedded_chunks


if __name__ == "__main__":
    from chunker import create_chunks
    from document_loader import load_pdf_pages

    pdf_file = "data/documents/Synthetic_Vendor_Services_Agreement.pdf"

    pages = load_pdf_pages(pdf_file)

    chunks = create_chunks(
        pages,
        chunk_size=500,
        overlap=100
    )

    model = load_embedding_model()

    embedded_chunks = create_embeddings(
        chunks,
        model
    )

    print("=" * 70)
    print("EMBEDDING TEST")
    print("=" * 70)

    print(f"\nTotal chunks    : {len(embedded_chunks)}")
    print(
        f"Embedding size  : "
        f"{len(embedded_chunks[0]['embedding'])}"
    )

    print(f"\nFirst chunk ID  : {embedded_chunks[0]['chunk_id']}")
    print(f"Page            : {embedded_chunks[0]['page']}")
    print(
        f"Vector preview  : "
        f"{embedded_chunks[0]['embedding'][:5]}"
    )

    print("\n" + "=" * 70)
    print("Embedding generation successful!")
    print("=" * 70)