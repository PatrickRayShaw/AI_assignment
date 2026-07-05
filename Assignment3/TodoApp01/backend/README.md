# Todo Backend

基于 FastAPI + SQLite

启动: uvicorn main:app --reload

API 接口:
- GET /todos?filter=all|completed|uncompleted
- POST /todos  { "title": "..." }
- PUT /todos/{id}  { "completed": true/false }
- DELETE /todos/{id}
- DELETE /todos?action=completed|all
