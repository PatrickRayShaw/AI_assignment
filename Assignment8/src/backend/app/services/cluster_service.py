from app.models.database import get_db
from collections import Counter
import json
import os
from datetime import datetime

class ClusterService:
    REPORT_PATH = 'data/cluster_report.json'
    
    def analyze(self, top_n=10):
        """Perform TF-IDF style keyword extraction and clustering"""
        conn = get_db()
        rows = conn.execute("SELECT id, title, content FROM news").fetchall()
        conn.close()
        
        if not rows:
            return {'error': '知识库为空，无法进行分析', 'keywords': [], 'total_news': 0}
        
        # Simple keyword extraction using jieba
        try:
            import jieba
            import jieba.analyse
            
            all_text = ' '.join([(r['title'] + ' ' + (r['content'] or '')) for r in rows])
            keywords = jieba.analyse.extract_tags(all_text, topK=top_n, withWeight=True)
            
            keyword_list = []
            for i, (word, weight) in enumerate(keywords):
                keyword_list.append({
                    'rank': i + 1,
                    'keyword': word,
                    'weight': round(weight, 4),
                    'percentage': round(weight / sum(w for _, w in keywords) * 100, 1)
                })
        except ImportError:
            # Fallback: simple word frequency
            all_text = ' '.join([(r['title'] + ' ' + (r['content'] or '')) for r in rows])
            words = [w for w in all_text.split() if len(w) >= 2]
            word_counts = Counter(words).most_common(top_n)
            total = sum(c for _, c in word_counts)
            keyword_list = []
            for i, (word, count) in enumerate(word_counts):
                keyword_list.append({
                    'rank': i + 1,
                    'keyword': word,
                    'weight': count,
                    'percentage': round(count / total * 100, 1) if total > 0 else 0
                })
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_news': len(rows),
            'top_n': top_n,
            'keywords': keyword_list
        }
        
        # Save report
        os.makedirs('data', exist_ok=True)
        with open(self.REPORT_PATH, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def get_latest_report(self):
        if os.path.exists(self.REPORT_PATH):
            with open(self.REPORT_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'error': '暂无分析报告，请先生成', 'keywords': [], 'total_news': 0}
