-- XU-News-AI-RAG 数据库建表脚本
-- 适用于 SQLite / MySQL

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 新闻表
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

-- 新闻标签表
CREATE TABLE IF NOT EXISTS news_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
);

-- 搜索日志表
CREATE TABLE IF NOT EXISTS search_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    query TEXT NOT NULL,
    results_count INTEGER DEFAULT 0,
    source TEXT DEFAULT 'local',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_news_created ON news(created_at);
CREATE INDEX IF NOT EXISTS idx_news_source_type ON news(source_type);
CREATE INDEX IF NOT EXISTS idx_news_tags_tag ON news_tags(tag);
CREATE INDEX IF NOT EXISTS idx_search_logs_created ON search_logs(created_at);

-- 初始化数据：管理员用户 (密码: admin123)
INSERT OR IGNORE INTO users (username, password_hash, email) VALUES
('admin', '$2b$12$LJ3m4ys3G.4qN8QmArHWlOcZ9xYmVj0qk5qvB6YwYh8J7V8qKd6a', 'admin@xu-news.local');

-- 示例新闻数据
INSERT OR IGNORE INTO news (title, content, source, source_type, url, summary) VALUES
('OpenAI发布GPT-5预览版', 'OpenAI于今日发布了GPT-5的预览版本，在推理能力和多模态处理方面有显著提升...', 'TechCrunch', 'rss', 'https://techcrunch.com/gpt5', 'GPT-5预览版发布'),
('量子计算新突破：1000量子比特', '科学家实现了1000量子比特的稳定纠缠...', 'Nature', 'web', 'https://nature.com/quantum1000', '量子计算里程碑'),
('全球网络安全态势报告2026', '2026年全球网络安全威胁持续增长...', 'Reuters', 'rss', 'https://reuters.com/cyber2026', '网络安全年度报告');

-- 示例标签
INSERT OR IGNORE INTO news_tags (news_id, tag) VALUES (1, 'AI'), (1, 'GPT'), (2, '量子'), (2, '科技'), (3, '安全');
