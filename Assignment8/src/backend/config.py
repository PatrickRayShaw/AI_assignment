import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'xu-news-ai-rag-secret-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-2026')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'data/xu_news.db')
    FAISS_INDEX_PATH = os.environ.get('FAISS_INDEX_PATH', 'data/faiss_index')
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    RERANK_MODEL = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = 'qwen2.5:3b'
    N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook')
    BAIDU_SEARCH_API = 'https://www.baidu.com/s'
    SIMILARITY_THRESHOLD = 0.6
    SEARCH_TOP_K = 10
