import yaml
import os
from pathlib import Path

# Load config from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "config.yaml"

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")
    
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

# Global Config Object
CONFIG = load_config()

# Helper Accessors
SERVER_HOST = CONFIG["server"]["host"]
SERVER_PORT = CONFIG["server"]["port"]
API_URL = CONFIG["server"]["api_url"]

DATA_DIR = CONFIG["paths"]["data_dir"]
INDEX_DIR_PDFS = CONFIG["paths"]["index_dir_pdfs"]
INDEX_DIR_EXAMPLES = CONFIG["paths"]["index_dir_examples"]
FEW_SHOT_DATA = CONFIG["paths"]["few_shot_data"]

EMBEDDING_MODEL = CONFIG["models"]["embedding_model"]

DOC_HALLUCINATION = CONFIG["documentation"]["hallucination_doc"]
DOC_TEMPERATURE = CONFIG["documentation"]["temperature_doc"]
DOC_SAMPLE_QUESTIONS = CONFIG["documentation"]["sample_questions_doc"]
DOC_PROMPTING = CONFIG["documentation"]["prompting_doc"]
DOC_RAG_CONCEPTS = CONFIG["documentation"]["rag_concepts_doc"]
