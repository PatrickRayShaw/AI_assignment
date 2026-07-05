import sqlite3
import os
from datetime import datetime
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            content TEXT,
            summary TEXT,
            source TEXT,
            source_type TEXT DEFAULT 'manual',
            url TEXT,
            vector_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        
        CREATE TABLE IF NOT EXISTS news_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
        );
        
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT NOT NULL,
            results_count INTEGER DEFAULT 0,
            source TEXT DEFAULT 'local',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_news_created ON news(created_at);
        CREATE INDEX IF NOT EXISTS idx_news_source_type ON news(source_type);
        CREATE INDEX IF NOT EXISTS idx_news_tags_tag ON news_tags(tag);
        CREATE INDEX IF NOT EXISTS idx_search_logs_created ON search_logs(created_at);
    """)
    
    conn.commit()
    conn.close()

class User:
    @staticmethod
    def create(username, password_hash, email=None):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    
    @staticmethod
    def find_by_username(username):
        conn = get_db()
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        return dict(row) if row else None

class News:
    @staticmethod
    def create(title, content, source, source_type='manual', url=None, summary=None, tags=None):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO news (title, content, source, source_type, url, summary) VALUES (?, ?, ?, ?, ?, ?)",
            (title, content, source, source_type, url, summary)
        )
        news_id = cursor.lastrowid
        
        if tags:
            for tag in tags:
                cursor.execute("INSERT INTO news_tags (news_id, tag) VALUES (?, ?)", (news_id, tag.strip()))
        
        conn.commit()
        conn.close()
        return news_id
    
    @staticmethod
    def get_all(page=1, per_page=20, source_type=None, tag=None, keyword=None):
        conn = get_db()
        query = "SELECT DISTINCT n.* FROM news n"
        params = []
        conditions = []
        
        if tag:
            query += " JOIN news_tags nt ON n.id = nt.news_id"
            conditions.append("nt.tag = ?")
            params.append(tag)
        
        where_clause = []
        if source_type and source_type != '全部类型':
            where_clause.append("n.source_type = ?")
            params.append(source_type)
        if keyword:
            where_clause.append("(n.title LIKE ? OR n.content LIKE ?)")
            params.extend([f'%{keyword}%', f'%{keyword}%'])
        
        if conditions:
            where_clause.extend(conditions)
        
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)
        
        query += " ORDER BY n.created_at DESC LIMIT ? OFFSET ?"
        params.extend([per_page, (page - 1) * per_page])
        
        rows = conn.execute(query, params).fetchall()
        
        # Get total count
        count_query = "SELECT COUNT(DISTINCT n.id) FROM news n"
        if tag:
            count_query += " JOIN news_tags nt ON n.id = nt.news_id"
        if where_clause:
            count_query += " WHERE " + " AND ".join(where_clause)
        total = conn.execute(count_query, params[:-2] if params else []).fetchone()[0]
        
        # Get tags for each news
        result = []
        for row in rows:
            item = dict(row)
            tags_rows = conn.execute("SELECT tag FROM news_tags WHERE news_id = ?", (item['id'],)).fetchall()
            item['tags'] = [r['tag'] for r in tags_rows]
            result.append(item)
        
        conn.close()
        return result, total
    
    @staticmethod
    def get_by_id(news_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM news WHERE id = ?", (news_id,)).fetchone()
        if row:
            item = dict(row)
            tags_rows = conn.execute("SELECT tag FROM news_tags WHERE news_id = ?", (news_id,)).fetchall()
            item['tags'] = [r['tag'] for r in tags_rows]
            conn.close()
            return item
        conn.close()
        return None
    
    @staticmethod
    def update(news_id, **kwargs):
        conn = get_db()
        allowed = ['title', 'content', 'summary', 'source', 'source_type', 'url']
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if updates:
            updates['updated_at'] = datetime.now().isoformat()
            set_clause = ', '.join(f"{k} = ?" for k in updates)
            conn.execute(f"UPDATE news SET {set_clause} WHERE id = ?", list(updates.values()) + [news_id])
        
        if 'tags' in kwargs:
            conn.execute("DELETE FROM news_tags WHERE news_id = ?", (news_id,))
            for tag in kwargs['tags']:
                conn.execute("INSERT INTO news_tags (news_id, tag) VALUES (?, ?)", (news_id, tag.strip()))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(news_id):
        conn = get_db()
        conn.execute("DELETE FROM news_tags WHERE news_id = ?", (news_id,))
        conn.execute("DELETE FROM news WHERE id = ?", (news_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def batch_delete(news_ids):
        conn = get_db()
        for nid in news_ids:
            conn.execute("DELETE FROM news_tags WHERE news_id = ?", (nid,))
            conn.execute("DELETE FROM news WHERE id = ?", (nid,))
        conn.commit()
        conn.close()

class NewsTag:
    @staticmethod
    def get_all_tags():
        conn = get_db()
        rows = conn.execute("SELECT DISTINCT tag, COUNT(*) as cnt FROM news_tags GROUP BY tag ORDER BY cnt DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

class SearchLog:
    @staticmethod
    def create(user_id, query, results_count, source='local'):
        conn = get_db()
        conn.execute(
            "INSERT INTO search_logs (user_id, query, results_count, source) VALUES (?, ?, ?, ?)",
            (user_id, query, results_count, source)
        )
        conn.commit()
        conn.close()
