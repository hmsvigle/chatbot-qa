import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

# Data files
QA_CSV_PATH = DATA_DIR / "qa.csv"
EMBEDDINGS_PATH = EMBEDDINGS_DIR / "embeddings.pkl"

# Model configuration
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_THRESHOLD = 0.7
EMBEDDING_DIMENSION = 384

# Ensure directories exist
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)