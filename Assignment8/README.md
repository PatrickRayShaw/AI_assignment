# XU-News-AI-RAG：个性化新闻智能知识库

基于 RAG（检索增强生成）技术的私有化新闻知识库系统，实现新闻自动采集、语义检索、大模型问答与知识聚类分析。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Element Plus |
| 后端 | Flask + JWT 认证 |
| 数据库 | SQLite |
| 向量检索 | FAISS |
| 本地模型 | Ollama (qwen2.5:3b) |
| 工作流 | n8n (私有化部署) |

## 项目结构

```
Assignment8/
├── PRD.md                     # 产品需求文档
├── 设计文档.md                 # 概要设计文档
├── README.md                  # 本文件
├── database/
│   └── init.sql               # 数据库初始化脚本
├── src/
│   ├── backend/               # Flask 后端
│   │   ├── app.py             # 应用入口
│   │   ├── config.py          # 配置文件
│   │   ├── requirements.txt   # Python 依赖
│   │   └── app/
│   │       ├── models/        # 数据模型
│   │       ├── routes/        # API 路由
│   │       └── services/      # 业务服务
│   └── frontend/              # Vue3 前端
│       ├── package.json
│       ├── vite.config.js
│       ├── index.html
│       └── src/
│           ├── api/           # API 封装
│           ├── router/        # 路由配置
│           ├── store/         # 状态管理
│           └── views/         # 页面组件
├── n8n-workflows/             # n8n 工作流 JSON
│   ├── news_collection.json   # 新闻采集入库
│   ├── semantic_search.json   # 语义检索
│   ├── web_fallback.json      # 联网兜底
│   ├── cluster_analysis.json  # 聚类分析
│   └── email_notify.json      # 邮件通知
├── tests/
│   ├── test_cases.md          # 测试用例
│   └── test_report.md         # 测试报告
├── workflows/
│   └── README.md              # 工作流说明
└── 原型/
    └── index.html             # 高保真原型
```

## 环境要求

- Python 3.10+
- Node.js 18+
- Ollama (本地部署 qwen2.5:3b)
- n8n (私有化部署)

## 快速开始

### 1. 初始化数据库

```bash
sqlite3 database/news.db < database/init.sql
```

### 2. 启动后端

```bash
cd src/backend
pip install -r requirements.txt
python app.py
```

### 3. 启动前端

```bash
cd src/frontend
npm install
npm run dev
```

### 4. 导入 n8n 工作流

将 `n8n-workflows/` 下的 JSON 文件导入 n8n 实例。

## API 文档

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/register` | POST | 用户注册 |
| `/api/knowledge/list` | GET | 知识库列表 |
| `/api/search/semantic` | POST | 语义检索 |
| `/api/search/web` | POST | 联网搜索 |
| `/api/cluster/analyze` | POST | 聚类分析 |

## 许可证

本项目为培训考核项目，仅供学习使用。
