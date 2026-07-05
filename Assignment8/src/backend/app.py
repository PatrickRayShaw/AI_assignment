from app import create_app
from app.models.database import init_db

app = create_app()

if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("XU-News-AI-RAG Backend Server")
    print("=" * 50)
    print("API Base: http://localhost:5000/api")
    print("Endpoints:")
    print("  POST /api/auth/register  - 用户注册")
    print("  POST /api/auth/login     - 用户登录")
    print("  GET  /api/auth/me        - 当前用户信息")
    print("  GET  /api/knowledge/list - 知识库列表")
    print("  POST /api/knowledge/create - 创建新闻")
    print("  PUT  /api/knowledge/<id> - 更新新闻")
    print("  DELETE /api/knowledge/<id> - 删除新闻")
    print("  POST /api/search/semantic - 语义检索")
    print("  POST /api/cluster/analyze - 聚类分析")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
