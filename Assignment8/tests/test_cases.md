# XU-News-AI-RAG 测试用例

## 1. API 测试用例

### 1.1 登录
- **前置条件**：用户已注册
- **输入**：{ "username": "admin", "password": "123456" }
- **预期输出**：status 200，返回token
- **实际结果**：200 OK，token正确

### 1.2 语义搜索
- **前置条件**：知识库至少有1条与"人工智能"相关的新闻
- **输入**：{ "query": "人工智能", "top_k": 5 }
- **预期输出**：返回最多5条结果，每条包含title、score、source
- **实际结果**：返回3条，score均>0.7

### 1.3 知识库添加
- **输入**：{ "title": "测试新闻", "content": "这是一条测试", "source": "test", "type": "科技" }
- **预期**：status 201，返回id
- **实际**：201 Created

## 2. n8n 工作流测试

### 2.1 news_collection
- 触发条件：手动触发
- 检查点：RSS读取成功、数据写入数据库、向量化成功
- 验证：查询数据库确认新记录存在，FAISS索引包含新向量

### 2.2 semantic_search
- 触发：POST /webhook-search
- 输入：{ "query": "量子计算" }
- 验证：返回的结果包含"量子"相关新闻，且相似度分数合理
