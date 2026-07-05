# TodoApp 技术架构文档

## 1. 技术栈
- **前端**: React 18 + Axios
- **后端**: FastAPI + SQLAlchemy
- **数据库**: SQLite
- **项目结构**: 前后端分离，backend/ + front/

## 2. 数据库设计（SQLite）
\\\sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0
);
\\\

## 3. API 接口说明
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /todos?filter=all/completed/uncompleted | 获取待办列表 |
| POST | /todos | 创建待办 { "title": "xxx" } |
| PUT | /todos/{id} | 更新待办状态 { "completed": true/false } |
| DELETE | /todos/{id} | 删除单个待办 |
| DELETE | /todos?action=completed/all | 清除已完成 / 清除全部 |

## 4. 前端架构
- App.js：主组件，管理状态和路由
- api.js：封装所有 API 调用
- App.css：现代简约样式
- 组件树：App > add-form, filter-bar, todo-list, clear-bar
