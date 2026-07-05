# -*- coding: utf-8 -*-
"""订单管理技能执行器"""

from typing import Any, Dict
from .repository import get_repository, STATUS_MAP


class OrderManagementExecutor:
    """订单管理技能执行器"""

    def __init__(self):
        self.repo = get_repository()

    def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行指定的 action"""
        actions = {
            "list_orders": self.list_orders,
            "get_order_detail": self.get_order_detail,
            "order_statistics": self.order_statistics,
            "create_order": self.create_order,
            "update_order_status": self.update_order_status,
        }

        if action not in actions:
            return {
                "success": False,
                "error": f"未知操作: {action}，支持的操作: {list(actions.keys())}"
            }

        try:
            result = actions[action](params)
            return {"success": True, "data": result}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"执行异常: {str(e)}"}

    def list_orders(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分页查询订单"""
        page = int(params.get("page", 1))
        page_size = int(params.get("page_size", 10))
        status = params.get("status")
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        keyword = params.get("keyword")

        result = self.repo.list_orders(
            page=page,
            page_size=page_size,
            status=status,
            start_date=start_date,
            end_date=end_date,
            keyword=keyword
        )

        # 翻译状态为中文
        for item in result["items"]:
            item["status_cn"] = STATUS_MAP.get(item["status"], item["status"])

        return result

    def get_order_detail(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """查询订单详情"""
        order_id = params.get("order_id")
        if not order_id:
            raise ValueError("缺少必填参数: order_id")

        order = self.repo.get_order_detail(order_id)
        if not order:
            raise ValueError(f"订单不存在: {order_id}")

        order["status_cn"] = STATUS_MAP.get(order["status"], order["status"])
        return order

    def order_statistics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """订单统计"""
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        group_by = params.get("group_by", "status")

        result = self.repo.order_statistics(
            start_date=start_date,
            end_date=end_date,
            group_by=group_by
        )

        # 翻译分组键为中文
        if group_by == "status":
            translated_groups = {}
            for k, v in result["groups"].items():
                cn_key = STATUS_MAP.get(k, k)
                translated_groups[cn_key] = v
            result["groups"] = translated_groups

        return result

    def create_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """创建订单"""
        customer_name = params.get("customer_name")
        customer_phone = params.get("customer_phone")
        items = params.get("items", [])

        if not customer_name:
            raise ValueError("缺少必填参数: customer_name")
        if not customer_phone:
            raise ValueError("缺少必填参数: customer_phone")
        if not items:
            raise ValueError("缺少必填参数: items")
        if not isinstance(items, list):
            raise ValueError("items 必须是数组")

        order = self.repo.create_order(customer_name, customer_phone, items)
        order["status_cn"] = STATUS_MAP.get(order["status"], order["status"])
        return order

    def update_order_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """更新订单状态"""
        order_id = params.get("order_id")
        new_status = params.get("new_status")

        if not order_id:
            raise ValueError("缺少必填参数: order_id")
        if not new_status:
            raise ValueError("缺少必填参数: new_status")

        order = self.repo.update_order_status(order_id, new_status)
        order["status_cn"] = STATUS_MAP.get(order["status"], order["status"])
        return order


# 模块级单例
_executor: OrderManagementExecutor = None


def get_executor() -> OrderManagementExecutor:
    global _executor
    if _executor is None:
        _executor = OrderManagementExecutor()
    return _executor
