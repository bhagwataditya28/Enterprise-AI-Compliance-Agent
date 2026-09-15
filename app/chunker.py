from document_loader import load_pdf_pages
from config import CHUNK_SIZE, CHUNK_OVERLAP


def create_chunks(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict]:
    """
    Split document text into overlapping chunks while
    preserving page metadata.

    Args:
        pages: List of pages returned by load_pdf_pages().
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of characters shared between chunks.

    Returns:
        List of chunks containing chunk ID, page number,
        and text.
    """

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    for page in pages:
        text = page["text"]

        start = 0
        chunk_number = 1

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "chunk_id": f"page_{page['page']}_chunk_{chunk_number}",
                    "page": page["page"],
                    "text": chunk_text
                })

            # Move forward while keeping overlap
            start += chunk_size - overlap
            chunk_number += 1

    return chunks


if __name__ == "__main__":
    pdf_file = "data/documents/Synthetic_Vendor_Services_Agreement.pdf"

    pages = load_pdf_pages(pdf_file)

    chunks = create_chunks(
       	pages,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    print("=" * 70)
    print("IMPROVED DOCUMENT CHUNKING TEST")
    print("=" * 70)

    print(f"\nTotal pages : {len(pages)}")
    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print("\n" + "-" * 70)
        print(f"Chunk ID : {chunk['chunk_id']}")
        print(f"Page     : {chunk['page']}")
        print(f"Length   : {len(chunk['text'])} characters")
        print(f"Text     : {chunk['text'][:350]}")

    print("\n" + "=" * 70)
    print("Improved chunking successful!")
    print("=" * 70)