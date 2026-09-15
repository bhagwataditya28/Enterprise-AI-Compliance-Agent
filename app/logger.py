import logging
from pathlib import Path

from config import PROCESSED_DIR


LOG_FILE = PROCESSED_DIR / "application.log"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger("compliance_agent")