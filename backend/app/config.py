import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_MODEL = "gpt-4.1-mini"

EMBEDDING_MODEL = "text-embedding-3-small"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 150

TOP_K = 5
RERANK_TOP_K = 3

DATA_PATH = "../data"
CHROMA_PATH = "../data/chroma"