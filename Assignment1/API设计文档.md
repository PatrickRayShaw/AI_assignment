# API 设计文档

## 1. 概述
本文档基于项目任务管理系统需求（lesson1-1 需求分析）及用户输入输出要求（lesson1-2）生成。系统采用前后端分离架构，提供 RESTful API 接口。

## 2. 基础信息
- Base URL: `/api/v1`
- 数据格式: JSON
- 认证方式: JWT Token（Bearer）
- 字符编码: UTF-8

## 3. 用户管理（User）

### 3.1 登录
- `POST /auth/login`
- 请求体：`{ "username": string, "password": string }`
- 响应：`{ "token": string, "user": { id, name, role, department } }`

### 3.2 获取用户列表
- `GET /users`
- 查询参数：`?department=部门&role=角色&page=1&size=20`
- 响应：`{ "total": int, "items": [User] }`

### 3.3 创建用户
- `POST /users`
- 请求体：`{ "name": string, "department": string, "role": "leader"|"member" }`
- 响应：`{ "id": string, ... }`

### 3.4 更新用户
- `PUT /users/:id`
- 请求体：部分字段
- 响应：更新后的用户对象

### 3.5 删除用户
- `DELETE /users/:id`
- 响应：`{ "success": true }`

## 4. 项目管理（Project）

### 4.1 获取项目列表
- `GET /projects`
- 查询参数：`?status=进行中&department=部门&page=1&size=20`
- 响应：`{ "total": int, "items": [Project] }`

### 4.2 创建项目
- `POST /projects`
- 请求体：`{ "name": string, "department": string, "plan_start": date, "plan_end": date, "dependencies": string[], "leader_id": string, "members": string[] }`
- 响应：创建的项目对象

### 4.3 获取项目详情
- `GET /projects/:id`
- 响应：项目完整信息（含进度表、任务列表）

### 4.4 更新项目
- `PUT /projects/:id`
- 请求体：支持更新状态、进度、实际时间、备注等
- 响应：更新后项目

### 4.5 删除项目
- `DELETE /projects/:id`
- 限制：仅可删除未开始且无依赖的项目

## 5. 任务管理（Task）

### 5.1 获取任务列表
- `GET /projects/:projectId/tasks`
- 查询参数：`?status=待办&assignee=成员ID`
- 响应：任务列表

### 5.2 创建任务
- `POST /projects/:projectId/tasks`
- 请求体：`{ "name": string, "assignee_id": string, "deadline": date, "priority": "高"|"中"|"低" }`

### 5.3 更新任务状态
- `PUT /tasks/:id`
- 请求体：`{ "status": "待办"|"进行中"|"已完成", "progress": int(0-100), "actual_end": date, "comment": string }`
- 自动触发里程碑检查和预警

### 5.4 批量更新任务进度
- `POST /tasks/batch-update`
- 请求体：`[{ "id": string, "progress": int }]`

## 6. 统计与看板（Dashboard）

### 6.1 项目概览统计
- `GET /dashboard/overview`
- 响应：`{ total_projects, completed, in_progress, delayed, overdue_tasks }`

### 6.2 项目进度可视化数据
- `GET /projects/:id/progress`
- 响应：`{ series: [{ name: string, data: [{ x: date, y: progress }] }] }`

### 6.3 部门分布
- `GET /dashboard/department-distribution`
- 响应：`[{ department, project_count, completion_rate }]`

## 7. 预警与通知（Alert）

### 7.1 获取预警列表
- `GET /alerts`
- 查询参数：`?type=逾期|进度延误|资源冲突&resolved=false`
- 响应：预警列表

### 7.2 标记预警已处理
- `PUT /alerts/:id/resolve`

### 7.3 发送通知（内部）
- `POST /notifications/send`
- 请求体：`{ "target_ids": string[], "title": string, "content": string }`

## 8. 数据模型

### 8.1 用户 (User)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string (uuid) | 主键 |
| name | string | 姓名 |
| department | string | 所属部门 |
| role | 'leader' | 'member' | 角色 |
| created_at | datetime | |
| updated_at | datetime | |

### 8.2 项目 (Project)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 主键 |
| name | string | 项目名称 |
| department | string | 部门 |
| status | '计划中'|'进行中'|'已完成'|'已暂停'|'已取消' | 状态 |
| leader_id | string | 负责人ID |
| member_ids | string[] | 成员ID列表 |
| plan_start | date | 计划开始 |
| plan_end | date | 计划结束 |
| actual_end | date | 实际结束 |
| duration_days | int | 用时（天） |
| completion_rate | float | 完成率(0-100) |
| milestone | string | 里程碑描述 |
| remark | string | 备注 |
| dependency_ids | string[] | 依赖项目ID |
| progress_logs | array | 进度记录 |

### 8.3 任务 (Task)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | |
| project_id | string | 所属项目 |
| name | string | 任务名 |
| assignee_id | string | 负责人 |
| status | '待办'|'进行中'|'已完成' | |
| priority | '高'|'中'|'低' | |
| deadline | date | 截止日期 |
| progress | int(0-100) | 进度 |
| actual_end | date | 实际完成 |
| comment | string | |

## 9. 错误码
| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 参数错误/校验失败 |
| 401 | 未登录或Token过期 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 冲突（如依赖未完成） |
| 422 | 无法处理的实体 |
| 500 | 服务器内部错误 |

## 10. 认证与权限
- 所有接口需在 Header 携带 `Authorization: Bearer <token>`
- 管理员（leader）可管理项目/任务/用户
- 成员（member）仅可更新自己被分配的任务状态和进度
- 预警通知可自动推送到 WebSocket 或轮询

---
*生成时间：2026-07-04 22:45 | 基于 lesson1-1, lesson1-2, lesson1-3 提示词生成*
