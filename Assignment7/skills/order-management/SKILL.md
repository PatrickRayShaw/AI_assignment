# order-management - 订单管理技能

## 技能描述
订单管理系统技能，支持订单查询、详情查看、统计、创建和状态更新。通过自然语言即可操作订单数据，无需手动编写 SQL 或命令行。

## trigger_keywords
[
  "订单", "查询订单", "订单查询", "查订单", "找订单", "搜订单", "搜索订单",
  "订单详情", "订单信息", "订单明细", "查看订单", "看订单", "订单内容",
  "订单统计", "统计订单", "订单汇总", "订单报表", "订单分析", "订单概况",
  "创建订单", "新建订单", "下单", "加订单", "添加订单", "录入订单",
  "更新订单", "修改订单", "改订单", "订单状态", "状态更新", "更改状态",
  "order", "list orders", "order detail", "order statistics", "create order",
  "update order", "order status", "new order", "add order",
  "购买", "买了", "买了什么", "买一个", "订购", "采购", "下单",
  "客户", "客户订单", "谁买了", "哪个客户",
  "待支付", "已支付", "发货", "已完成", "pending", "paid", "shipped", "completed",
  "最近订单", "全部订单", "所有订单", "我的订单",
  "多少钱", "金额", "总价", "价格", "消费", "花费",
  "几月份", "这个月", "上个月", "统计一下"
]

## 参数定义

### list_orders - 分页查询订单列表
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 10 | 每页数量 |
| status | string | 否 | None | 状态筛选: pending/paid/shipped/completed |
| start_date | string | 否 | None | 开始日期 YYYY-MM-DD |
| end_date | string | 否 | None | 结束日期 YYYY-MM-DD |
| keyword | string | 否 | None | 关键词搜索(客户名/订单号) |

### get_order_detail - 查询订单详情
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| order_id | string | 是 | - | 订单ID |

### order_statistics - 订单统计
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| start_date | string | 否 | None | 开始日期 |
| end_date | string | 否 | None | 结束日期 |
| group_by | string | 否 | status | 分组维度: status/date/category |

### create_order - 创建订单
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| customer_name | string | 是 | - | 客户姓名 |
| customer_phone | string | 是 | - | 客户电话 |
| items | array | 是 | - | 商品列表 [{"name":"xx","price":99,"quantity":2}] |

### update_order_status - 更新订单状态
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| order_id | string | 是 | - | 订单ID |
| new_status | string | 是 | - | 新状态: pending/paid/shipped/completed |

## 使用示例

### 查询订单
- "帮我查一下最近的订单"
- "查询所有待支付的订单"
- "搜索张三的订单"
- "查一下2024年2月份的订单"
- "list all orders"
- "show me recent orders"
- "找一下已发货的订单"

### 订单详情
- "我想看订单ORD20240115001的详细信息"
- "查看订单ORD20240201001"
- "show order detail for ORD20240115001"
- "订单1的明细是什么"

### 创建订单
- "帮我创建一个新订单，客户李四，电话13800138002，买一个蓝牙耳机599元"
- "下单：客户王五，电话13800138003，购买机械键盘1299元"
- "新订单：张三 13800138001 iPhone手机壳 49.5元 x2"
- "create a new order for customer Li Si"

### 更新状态
- "把订单ORD20240215001的状态改为已支付"
- "更新订单1的状态为发货中"
- "将订单ORD20240301001改为已完成"
- "把待支付的订单标记为已支付"
- "update order ORD20240215001 to paid"

### 统计分析
- "统计一下二月份的订单情况"
- "统计所有订单，按状态分组"
- "分析一下最近的订单数据"
- "给我一个订单汇总报表"
- "show order statistics for January 2024"

## 状态流转规则
```
pending (待支付) → paid (已支付)
paid (已支付) → shipped (发货中)
shipped (发货中) → completed (已完成)
pending/paid → cancelled (已取消)
```

## Agent 交互说明

### 如何被 LLM 识别和调用
1. 当用户提到上述任意 trigger_keywords 时，LLM 应自动匹配此技能
2. LLM 从用户输入中提取参数（order_id、状态、日期等）
3. 调用对应的 action 函数
4. 将返回结果用自然语言呈现给用户

### 参数提取指南
- "最近的订单" → list_orders（默认参数）
- "订单ORD20240115001的详情" → get_order_detail(order_id="ORD20240115001")
- "待支付的订单" → list_orders(status="pending")
- "二月份的订单统计" → order_statistics(start_date="2024-02-01", end_date="2024-02-28")
- "创建订单，客户XX，电话XX，买XX" → create_order(...)
- "把订单X改为已支付" → update_order_status(order_id="X", new_status="paid")

### 自然语言表达覆盖（至少10种，用于Agent测试）

1. "查询订单" → list_orders
2. "帮我查一下最近的订单" → list_orders
3. "显示所有待支付的订单" → list_orders(status="pending")
4. "我要看订单ORD20240115001" → get_order_detail(order_id="ORD20240115001")
5. "张三买了什么" → list_orders(keyword="张三")
6. "统计二月份订单" → order_statistics(start_date="2024-02-01", end_date="2024-02-28")
7. "下单买蓝牙耳机" → create_order
8. "把订单状态改成已支付" → update_order_status
9. "分析一下最近的订单数据" → order_statistics
10. "最近有多少订单" → list_orders
11. "显示所有已完成的订单" → list_orders(status="completed")
12. "帮我看看ORD20240301001" → get_order_detail(order_id="ORD20240301001")
