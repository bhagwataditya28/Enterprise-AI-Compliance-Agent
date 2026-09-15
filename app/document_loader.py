from pathlib import Path
from pypdf import PdfReader


def load_pdf_pages(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF and preserve page numbers.

    Returns:
        A list of dictionaries containing page number and text.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    try:
        reader = PdfReader(path)
    except Exception as e:
        raise ValueError(
            f"Unable to read PDF file: {path}. "
            f"The file may be corrupted or invalid. "
            f"Details: {e}"
        ) from e

    if len(reader.pages) == 0:
        raise ValueError(
            f"The PDF contains no pages: {path}"
        )

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text.strip()
        })

    if not any(page["text"] for page in pages):
        raise ValueError(
            "No readable text could be extracted from the PDF. "
            "The document may be scanned, image-only, or empty."
        )

    return pages


if __name__ == "__main__":
    pdf_file = "data/documents/Synthetic_Vendor_Services_Agreement.pdf"

    pages = load_pdf_pages(pdf_file)

    print("=" * 70)
    print("STRUCTURED PDF EXTRACTION TEST")
    print("=" * 70)

    print(f"\nTotal pages: {len(pages)}")

    for page in pages:
        print(f"\n--- PAGE {page['page']} ---")
        print(page["text"][:500])

    print("\n" + "=" * 70)
    print("Extraction successful!")
    print("=" * 70)