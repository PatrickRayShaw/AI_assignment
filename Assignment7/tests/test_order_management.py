# -*- coding: utf-8 -*-
"""
订单管理技能测试 - 覆盖5个核心功能
通过 executor.execute() 调用，测试完整的 dispatch 路径
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from order_management.executor import OrderManagementExecutor
from order_management.repository import STATUS_MAP, STATUS_TRANSITIONS


@pytest.fixture
def executor():
    """创建执行器实例（每个测试独立）"""
    return OrderManagementExecutor()


# ========== list_orders ==========

class TestListOrders:
    """订单列表查询测试"""

    def test_list_all(self, executor):
        """查询全部订单"""
        result = executor.execute("list_orders", {})
        assert result["success"] is True
        assert result["data"]["total"] == 8
        assert len(result["data"]["items"]) == 8

    def test_list_pagination(self, executor):
        """分页查询"""
        result = executor.execute("list_orders", {"page": 1, "page_size": 3})
        assert result["success"] is True
        assert len(result["data"]["items"]) == 3
        assert result["data"]["page"] == 1

    def test_list_filter_by_status(self, executor):
        """按状态筛选"""
        result = executor.execute("list_orders", {"status": "pending"})
        assert result["success"] is True
        assert result["data"]["total"] == 2
        for o in result["data"]["items"]:
            assert o["status"] == "pending"

    def test_list_filter_by_date(self, executor):
        """按日期范围筛选"""
        result = executor.execute("list_orders", {
            "start_date": "2024-02-01",
            "end_date": "2024-02-29"
        })
        assert result["success"] is True
        assert result["data"]["total"] == 3

    def test_list_filter_by_keyword(self, executor):
        """按关键词搜索"""
        result = executor.execute("list_orders", {"keyword": "张三"})
        assert result["success"] is True
        assert result["data"]["total"] == 1

    def test_list_empty_result(self, executor):
        """无匹配结果"""
        result = executor.execute("list_orders", {"keyword": "不存在的人"})
        assert result["success"] is True
        assert result["data"]["total"] == 0


# ========== get_order_detail ==========

class TestGetOrderDetail:
    """订单详情查询测试"""

    def test_get_existing(self, executor):
        """查询存在的订单"""
        result = executor.execute("get_order_detail", {"order_id": "ORD20240115001"})
        assert result["success"] is True
        assert result["data"]["customer_name"] == "张三"
        assert result["data"]["total_amount"] == 299.00

    def test_get_nonexistent(self, executor):
        """查询不存在的订单"""
        result = executor.execute("get_order_detail", {"order_id": "ORD99999999"})
        assert result["success"] is False
        assert "不存在" in result["error"]

    def test_get_missing_id(self, executor):
        """缺少 order_id"""
        result = executor.execute("get_order_detail", {})
        assert result["success"] is False


# ========== order_statistics ==========

class TestOrderStatistics:
    """订单统计测试"""

    def test_statistics_all(self, executor):
        """全部统计"""
        result = executor.execute("order_statistics", {})
        assert result["success"] is True
        assert result["data"]["total_orders"] == 8
        assert result["data"]["total_amount"] > 0

    def test_statistics_by_status(self, executor):
        """按状态分组"""
        result = executor.execute("order_statistics", {"group_by": "status"})
        assert result["success"] is True
        assert len(result["data"]["groups"]) >= 4

    def test_statistics_by_date(self, executor):
        """按日期分组"""
        result = executor.execute("order_statistics", {"group_by": "date"})
        assert result["success"] is True

    def test_statistics_date_filter(self, executor):
        """带日期过滤的统计"""
        result = executor.execute("order_statistics", {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        })
        assert result["success"] is True
        assert result["data"]["total_orders"] == 2  # Jan has 2 orders


# ========== create_order ==========

class TestCreateOrder:
    """订单创建测试"""

    def test_create_success(self, executor):
        """成功创建订单"""
        result = executor.execute("create_order", {
            "customer_name": "测试用户",
            "customer_phone": "13800000000",
            "items": [{"name": "测试商品", "price": 100, "quantity": 2}]
        })
        assert result["success"] is True
        assert result["data"]["status"] == "pending"
        assert result["data"]["total_amount"] == 200.00
        assert result["data"]["order_id"].startswith("ORD")

    def test_create_missing_name(self, executor):
        """缺少客户名"""
        result = executor.execute("create_order", {
            "customer_name": "",
            "customer_phone": "13800000000",
            "items": [{"name": "商品", "price": 10, "quantity": 1}]
        })
        assert result["success"] is False

    def test_create_missing_phone(self, executor):
        """缺少电话"""
        result = executor.execute("create_order", {
            "customer_name": "测试",
            "customer_phone": "",
            "items": [{"name": "商品", "price": 10, "quantity": 1}]
        })
        assert result["success"] is False

    def test_create_empty_items(self, executor):
        """空商品列表"""
        result = executor.execute("create_order", {
            "customer_name": "测试",
            "customer_phone": "13800000000",
            "items": []
        })
        assert result["success"] is False


# ========== update_order_status ==========

class TestUpdateOrderStatus:
    """订单状态更新测试"""

    def test_update_pending_to_paid(self, executor):
        """待支付→已支付"""
        result = executor.execute("update_order_status", {
            "order_id": "ORD20240215001",  # pending
            "new_status": "paid"
        })
        assert result["success"] is True
        assert result["data"]["status"] == "paid"

    def test_update_paid_to_shipped(self, executor):
        """已支付→发货中"""
        result = executor.execute("update_order_status", {
            "order_id": "ORD20240201001",  # paid
            "new_status": "shipped"
        })
        assert result["success"] is True

    def test_update_invalid_transition(self, executor):
        """无效状态流转（pending→completed 跳过中间状态）"""
        result = executor.execute("update_order_status", {
            "order_id": "ORD20240215001",  # pending
            "new_status": "completed"
        })
        assert result["success"] is False
        assert "不允许" in result["error"]

    def test_update_completed_no_change(self, executor):
        """已完成订单不可再流转"""
        result = executor.execute("update_order_status", {
            "order_id": "ORD20240115001",  # completed
            "new_status": "paid"
        })
        assert result["success"] is False

    def test_update_nonexistent(self, executor):
        """不存在的订单"""
        result = executor.execute("update_order_status", {
            "order_id": "ORD99999999",
            "new_status": "paid"
        })
        assert result["success"] is False


# ========== execute dispatch ==========

class TestExecuteDispatch:
    """execute 分发测试"""

    def test_valid_action(self, executor):
        result = executor.execute("list_orders", {})
        assert result["success"] is True

    def test_invalid_action(self, executor):
        result = executor.execute("nonexistent_action", {})
        assert result["success"] is False
        assert "未知操作" in result["error"]
