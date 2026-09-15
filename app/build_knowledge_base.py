import json
from pathlib import Path

from document_loader import load_pdf_pages
from chunker import create_chunks
from embeddings import load_embedding_model, create_embeddings
from config import (
    DEFAULT_CONTRACT,
    KNOWLEDGE_BASE_FILE,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


DEFAULT_PDF_FILE = DEFAULT_CONTRACT
DEFAULT_OUTPUT_FILE = KNOWLEDGE_BASE_FILE

def build_knowledge_base(
    pdf_file: str = DEFAULT_PDF_FILE,
    output_file: str = DEFAULT_OUTPUT_FILE
):
    print("=" * 70)
    print("BUILDING KNOWLEDGE BASE")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Load PDF
    # ---------------------------------------------------------
    print("\n[1/5] Loading PDF...")

    pages = load_pdf_pages(pdf_file)

    print(f"Total pages found: {len(pages)}")

    # ---------------------------------------------------------
    # 2. Remove testing / answer-key page
    # ---------------------------------------------------------
    print("\n[2/5] Removing testing notes...")

    clean_pages = [
        page
        for page in pages
        if page["page"] != 3
    ]

    print(f"Pages used for knowledge base: {len(clean_pages)}")

    # ---------------------------------------------------------
    # 3. Create chunks
    # ---------------------------------------------------------
    print("\n[3/5] Creating chunks...")

    chunks = create_chunks(
        clean_pages,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    print(f"Total chunks created: {len(chunks)}")

    # ---------------------------------------------------------
    # 4. Generate embeddings
    # ---------------------------------------------------------
    print("\n[4/5] Generating embeddings...")

    model = load_embedding_model()

    embedded_chunks = create_embeddings(
        chunks,
        model
    )

    print(f"Embeddings generated: {len(embedded_chunks)}")

    # ---------------------------------------------------------
    # 5. Save knowledge base
    # ---------------------------------------------------------
    print("\n[5/5] Saving knowledge base...")

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            embedded_chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nKnowledge base saved to:")
    print(output_path)

    print("\n" + "=" * 70)
    print("KNOWLEDGE BASE BUILD SUCCESSFUL!")
    print("=" * 70)

    return embedded_chunks


if __name__ == "__main__":
    build_knowledge_base()