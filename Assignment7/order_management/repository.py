# -*- coding: utf-8 -*-
"""订单数据仓库 - 模拟数据库操作"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional

# 模拟订单数据
MOCK_ORDERS = [
    {
        "order_id": "ORD20240115001",
        "customer_name": "张三",
        "customer_phone": "13800138001",
        "status": "completed",
        "total_amount": 299.00,
        "create_time": "2024-01-15 14:30:00",
        "items": [
            {"name": "iPhone手机壳", "price": 49.50, "quantity": 2, "category": "手机配件"},
            {"name": "钢化膜", "price": 40.00, "quantity": 5, "category": "手机配件"}
        ]
    },
    {
        "order_id": "ORD20240120001",
        "customer_name": "李四",
        "customer_phone": "13800138002",
        "status": "shipped",
        "total_amount": 599.00,
        "create_time": "2024-01-20 10:15:00",
        "items": [
            {"name": "蓝牙耳机", "price": 599.00, "quantity": 1, "category": "数码产品"}
        ]
    },
    {
        "order_id": "ORD20240201001",
        "customer_name": "王五",
        "customer_phone": "13800138003",
        "status": "paid",
        "total_amount": 1299.00,
        "create_time": "2024-02-01 09:00:00",
        "items": [
            {"name": "机械键盘", "price": 899.00, "quantity": 1, "category": "电脑外设"},
            {"name": "鼠标垫", "price": 100.00, "quantity": 4, "category": "电脑外设"}
        ]
    },
    {
        "order_id": "ORD20240215001",
        "customer_name": "赵六",
        "customer_phone": "13800138004",
        "status": "pending",
        "total_amount": 158.00,
        "create_time": "2024-02-15 16:45:00",
        "items": [
            {"name": "USB数据线", "price": 39.50, "quantity": 4, "category": "手机配件"}
        ]
    },
    {
        "order_id": "ORD20240228001",
        "customer_name": "孙七",
        "customer_phone": "13800138005",
        "status": "completed",
        "total_amount": 1999.00,
        "create_time": "2024-02-28 11:20:00",
        "items": [
            {"name": "显示器支架", "price": 999.00, "quantity": 1, "category": "办公设备"},
            {"name": "台灯", "price": 500.00, "quantity": 2, "category": "办公设备"}
        ]
    },
    {
        "order_id": "ORD20240301001",
        "customer_name": "周八",
        "customer_phone": "13800138006",
        "status": "shipped",
        "total_amount": 349.00,
        "create_time": "2024-03-01 08:30:00",
        "items": [
            {"name": "保温杯", "price": 349.00, "quantity": 1, "category": "生活用品"}
        ]
    },
    {
        "order_id": "ORD20240315001",
        "customer_name": "朱十六",
        "customer_phone": "13800138007",
        "status": "shipped",
        "total_amount": 699.00,
        "create_time": "2024-03-15 13:00:00",
        "items": [
            {"name": "背包", "price": 699.00, "quantity": 1, "category": "生活用品"}
        ]
    },
    {
        "order_id": "ORD20240320001",
        "customer_name": "徐十七",
        "customer_phone": "13800138008",
        "status": "pending",
        "total_amount": 399.00,
        "create_time": "2024-03-20 17:00:00",
        "items": [
            {"name": "运动鞋", "price": 399.00, "quantity": 1, "category": "服装鞋帽"}
        ]
    }
]

STATUS_MAP = {
    "pending": "待支付",
    "paid": "已支付",
    "shipped": "发货中",
    "completed": "已完成"
}

STATUS_TRANSITIONS = {
    "pending": ["paid", "cancelled"],
    "paid": ["shipped", "cancelled"],
    "shipped": ["completed"],
    "completed": []
}


class OrderRepository:
    """订单数据仓库"""

    def __init__(self):
        self._orders = [dict(o) for o in MOCK_ORDERS]
        self._id_counter = max(
            int(o["order_id"][3:11] + o["order_id"][11:]) 
            for o in MOCK_ORDERS
        ) if MOCK_ORDERS else 20240101001

    def _generate_order_id(self) -> str:
        """生成订单号 ORD + 日期 + 序号"""
        self._id_counter += 1
        return f"ORD{self._id_counter}"

    def list_orders(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> dict:
        """分页查询订单"""
        filtered = self._orders[:]

        if status:
            filtered = [o for o in filtered if o["status"] == status]
        if start_date:
            filtered = [o for o in filtered if o["create_time"][:10] >= start_date]
        if end_date:
            filtered = [o for o in filtered if o["create_time"][:10] <= end_date]
        if keyword:
            filtered = [
                o for o in filtered
                if keyword.lower() in o["order_id"].lower()
                or keyword.lower() in o["customer_name"].lower()
            ]

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        items = filtered[start:end]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
            "items": items
        }

    def get_order_detail(self, order_id: str) -> Optional[dict]:
        """获取订单详情"""
        for o in self._orders:
            if o["order_id"] == order_id:
                return dict(o)
        return None

    def order_statistics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: str = "status"
    ) -> dict:
        """订单统计"""
        filtered = self._orders[:]
        if start_date:
            filtered = [o for o in filtered if o["create_time"][:10] >= start_date]
        if end_date:
            filtered = [o for o in filtered if o["create_time"][:10] <= end_date]

        total_orders = len(filtered)
        total_amount = sum(o["total_amount"] for o in filtered)
        avg_amount = total_amount / total_orders if total_orders > 0 else 0

        groups = {}
        for o in filtered:
            if group_by == "status":
                key = o["status"]
            elif group_by == "date":
                key = o["create_time"][:10]
            elif group_by == "category":
                for item in o["items"]:
                    cat = item.get("category", "未分类")
                    if cat not in groups:
                        groups[cat] = {"count": 0, "total_amount": 0.0}
                    groups[cat]["count"] += 1
                    groups[cat]["total_amount"] += item["price"] * item["quantity"]
                continue
            else:
                key = o.get(group_by, "unknown")

            if key not in groups:
                groups[key] = {"count": 0, "total_amount": 0.0}
            groups[key]["count"] += 1
            groups[key]["total_amount"] += o["total_amount"]

        return {
            "total_orders": total_orders,
            "total_amount": round(total_amount, 2),
            "avg_amount": round(avg_amount, 2),
            "group_by": group_by,
            "groups": groups
        }

    def create_order(
        self,
        customer_name: str,
        customer_phone: str,
        items: list
    ) -> dict:
        """创建订单"""
        total_amount = sum(
            item.get("price", 0) * item.get("quantity", 1)
            for item in items
        )
        order = {
            "order_id": self._generate_order_id(),
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "status": "pending",
            "total_amount": round(total_amount, 2),
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": items
        }
        self._orders.append(order)
        return dict(order)

    def update_order_status(self, order_id: str, new_status: str) -> Optional[dict]:
        """更新订单状态"""
        order = self.get_order_detail(order_id)
        if not order:
            return None

        old_status = order["status"]
        if new_status not in STATUS_TRANSITIONS.get(old_status, []):
            raise ValueError(
                f"不允许从 '{old_status}' 变更到 '{new_status}'。"
                f"允许的变更: {STATUS_TRANSITIONS.get(old_status, [])}"
            )

        order["status"] = new_status
        return dict(order)


# 全局单例
_repository: Optional[OrderRepository] = None


def get_repository() -> OrderRepository:
    global _repository
    if _repository is None:
        _repository = OrderRepository()
    return _repository
