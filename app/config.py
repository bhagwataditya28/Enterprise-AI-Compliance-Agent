from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "qwen3:4b"


# Retrieval settings
TOP_K = 5


# Chunking settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# Default files
DEFAULT_CONTRACT = (
    DOCUMENTS_DIR / "Synthetic_Vendor_Services_Agreement.pdf"
)

KNOWLEDGE_BASE_FILE = (
    PROCESSED_DIR / "knowledge_base.json"
)

REPORT_FILE = (
    PROCESSED_DIR / "contract_risk_report.txt"
)