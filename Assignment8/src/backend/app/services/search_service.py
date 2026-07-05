import requests
import numpy as np
from sentence_transformers import SentenceTransformer
from config import Config
from app.models.database import get_db

class SearchService:
    def __init__(self):
        self.embedding_model = None
        self.similarity_threshold = Config.SIMILARITY_THRESHOLD
        self.top_k = Config.SEARCH_TOP_K
    
    def _load_embedding_model(self):
        if self.embedding_model is None:
            try:
                self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
            except Exception as e:
                print(f"Warning: Could not load embedding model: {e}")
        return self.embedding_model
    
    def search(self, query):
        model = self._load_embedding_model()
        results = {'query': query, 'source': 'local', 'items': []}
        
        if model:
            # Local FAISS search
            try:
                import faiss
                import os
                index_path = Config.FAISS_INDEX_PATH
                
                if os.path.exists(f"{index_path}.index"):
                    index = faiss.read_index(f"{index_path}.index")
                    query_embedding = model.encode([query], convert_to_numpy=True)
                    query_embedding = query_embedding.astype(np.float32)
                    faiss.normalize_L2(query_embedding)
                    
                    distances, indices = index.search(query_embedding, self.top_k)
                    
                    conn = get_db()
                    local_results = []
                    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
                        if idx < 0:
                            continue
                        similarity = float(1 - dist / 2)  # cosine similarity from L2
                        if similarity >= self.similarity_threshold:
                            row = conn.execute(
                                "SELECT n.*, GROUP_CONCAT(nt.tag) as tags FROM news n "
                                "LEFT JOIN news_tags nt ON n.id = nt.news_id "
                                "WHERE n.id = ? GROUP BY n.id", (int(idx + 1),)
                            ).fetchone()
                            if row:
                                item = dict(row)
                                item['similarity'] = round(similarity * 100, 1)
                                item['tags'] = item['tags'].split(',') if item['tags'] else []
                                local_results.append(item)
                    conn.close()
                    
                    if local_results:
                        results['items'] = local_results
                        return results
            except Exception as e:
                print(f"FAISS search error: {e}")
        
        # Fallback to web search
        results['source'] = 'web'
        results['items'] = self._web_search(query)
        return results
    
    def _web_search(self, query):
        """Baidu search + Ollama reasoning fallback"""
        try:
            # Try Ollama for direct reasoning
            ollama_resp = requests.post(
                f"{Config.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": Config.OLLAMA_MODEL,
                    "prompt": f"请根据以下问题，整合你已知的知识给出简要回答（不超过300字）：\n\n{query}",
                    "stream": False
                },
                timeout=30
            )
            if ollama_resp.status_code == 200:
                answer = ollama_resp.json().get('response', '')
                return [{
                    'title': 'AI智能回答（联网兜底）',
                    'content': answer,
                    'source': 'Ollama ' + Config.OLLAMA_MODEL,
                    'similarity': 100.0,
                    'tags': ['联网搜索', 'AI推理']
                }]
        except Exception as e:
            print(f"Ollama fallback error: {e}")
        
        # Ultimate fallback
        return [{
            'title': '联网搜索提示',
            'content': f'知识库中暂无与"{query}"匹配的内容。建议：1) 检查拼写 2) 尝试更宽泛的关键词 3) 手动添加相关新闻到知识库',
            'source': 'system',
            'similarity': 0,
            'tags': ['系统提示']
        }]
