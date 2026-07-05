# -*- coding: utf-8 -*-
"""订单管理系统 - API 控制器 / 独立运行入口"""

import sys
import os
import json

# 确保当前目录在 path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order_management.executor import get_executor
from order_management.repository import STATUS_MAP


def format_order_list(data: dict) -> str:
    """格式化订单列表为可读文本"""
    lines = []
    lines.append(f"共找到 {data['total']} 条订单 (第{data['page']}/{data['total_pages']}页):")
    lines.append("-" * 60)
    for i, order in enumerate(data["items"], 1):
        lines.append(
            f"  {i}. {order['order_id']} - {order['customer_name']} - "
            f"¥{order['total_amount']:.2f} - {order.get('status_cn', order['status'])}"
        )
    return "\n".join(lines)


def format_order_detail(order: dict) -> str:
    """格式化订单详情为可读文本"""
    lines = []
    lines.append(f"订单 {order['order_id']} 的详细信息:")
    lines.append(f"  客户: {order['customer_name']}")
    lines.append(f"  电话: {order['customer_phone']}")
    lines.append(f"  金额: ¥{order['total_amount']:.2f}")
    lines.append(f"  状态: {order.get('status_cn', order['status'])}")
    lines.append(f"  时间: {order['create_time']}")
    lines.append(f"  商品明细:")
    for item in order["items"]:
        lines.append(
            f"    - {item['name']} x{item['quantity']} = "
            f"¥{item['price'] * item['quantity']:.2f}"
        )
    return "\n".join(lines)


def format_statistics(data: dict) -> str:
    """格式化统计结果为可读文本"""
    lines = []
    lines.append(f"订单统计 (分组: {data['group_by']}):")
    lines.append(f"  总订单数: {data['total_orders']} 笔")
    lines.append(f"  总金额: ¥{data['total_amount']:.2f}")
    lines.append(f"  平均金额: ¥{data['avg_amount']:.2f}")
    lines.append(f"  分组明细:")
    for group_name, group_data in data.get("groups", {}).items():
        lines.append(
            f"    {group_name}: {group_data['count']}笔, "
            f"¥{group_data['total_amount']:.2f}"
        )
    return "\n".join(lines)


def handle_command(cmd_input: str) -> str:
    """处理命令输入（供 chat_agent 调用）"""
    executor = get_executor()

    # 简单规则匹配（实际应由 LLM 完成意图识别）
    cmd_lower = cmd_input.strip().lower()

    if "创建" in cmd_input or "create" in cmd_lower:
        # 尝试从输入中提取信息
        return handle_create_order(cmd_input, executor)

    elif "统计" in cmd_input or "statistics" in cmd_lower:
        params = parse_statistics_params(cmd_input)
        result = executor.execute("order_statistics", params)
        if result["success"]:
            return format_statistics(result["data"])
        return f"统计失败: {result['error']}"

    elif "更新" in cmd_input or "update" in cmd_lower or "状态" in cmd_input:
        params = parse_update_params(cmd_input)
        if not params.get("order_id"):
            return "请指定要更新的订单ID"
        if not params.get("new_status"):
            return "请指定新状态 (pending/paid/shipped/completed)"
        result = executor.execute("update_order_status", params)
        if result["success"]:
            order = result["data"]
            return f"订单状态已更新: {order['order_id']} -> {order.get('status_cn', order['status'])}"
        return f"更新失败: {result['error']}"

    elif "详情" in cmd_input or "detail" in cmd_lower or "详细信息" in cmd_input:
        # 提取订单ID
        import re
        order_ids = re.findall(r'ORD\d+', cmd_input.upper())
        if order_ids:
            result = executor.execute("get_order_detail", {"order_id": order_ids[0]})
            if result["success"]:
                return format_order_detail(result["data"])
            return f"查询失败: {result['error']}"
        return "请提供订单ID"

    else:
        # 默认按查询处理
        params = parse_list_params(cmd_input)
        result = executor.execute("list_orders", params)
        if result["success"]:
            return format_order_list(result["data"])
        return f"查询失败: {result['error']}"


def handle_create_order(cmd_input: str, executor) -> str:
    """处理创建订单"""
    import re

    # 提取客户名
    name_match = re.search(r'客户[：:]?\s*(\S+)', cmd_input)
    phone_match = re.search(r'电话[：:]?\s*(\d{11})', cmd_input)

    # 提取商品信息
    items = []
    # 匹配类似 "蓝牙耳机599元" 或 "商品名x2=100元"
    item_pattern = re.findall(r'([\u4e00-\u9fa5a-zA-Z0-9]+)\s*(\d+)\s*元', cmd_input)
    for name, price in item_pattern:
        items.append({"name": name.strip(), "price": float(price), "quantity": 1})

    if not name_match:
        return "请提供客户姓名 (格式: 客户XX)"
    if not phone_match:
        return "请提供客户电话 (格式: 电话138xxxxxxxxx)"
    if not items:
        return "请提供商品信息 (格式: 商品名 价格 元)"

    params = {
        "customer_name": name_match.group(1),
        "customer_phone": phone_match.group(1),
        "items": items
    }
    result = executor.execute("create_order", params)
    if result["success"]:
        order = result["data"]
        return f"订单创建成功!\n  订单号: {order['order_id']}\n  总金额: ¥{order['total_amount']:.2f}"
    return f"创建失败: {result['error']}"


def parse_list_params(cmd_input: str) -> dict:
    """解析查询参数"""
    params = {"page": 1, "page_size": 10}
    import re

    # 提取页码
    page_match = re.search(r'第?\s*(\d+)\s*页', cmd_input)
    if page_match:
        params["page"] = int(page_match.group(1))

    # 状态筛选
    for status_key, status_cn in STATUS_MAP.items():
        if status_cn in cmd_input:
            params["status"] = status_key
            break

    return params


def parse_statistics_params(cmd_input: str) -> dict:
    """解析统计参数"""
    params = {}
    import re

    # 提取月份
    month_match = re.search(r'(\d+)\s*月', cmd_input)
    if month_match:
        month = int(month_match.group(1))
        year = 2024  # 默认年份
        year_match = re.search(r'(\d{4})\s*年', cmd_input)
        if year_match:
            year = int(year_match.group(1))
        start_day = f"{year}-{month:02d}-01"
        # 计算月末
        import calendar
        last_day = calendar.monthrange(year, month)[1]
        end_day = f"{year}-{month:02d}-{last_day:02d}"
        params["start_date"] = start_day
        params["end_date"] = end_day

    # 分组维度
    if "日期" in cmd_input or "date" in cmd_input.lower():
        params["group_by"] = "date"
    elif "类别" in cmd_input or "category" in cmd_input.lower():
        params["group_by"] = "category"
    else:
        params["group_by"] = "status"

    return params


def parse_update_params(cmd_input: str) -> dict:
    """解析更新参数"""
    import re
    params = {}

    # 提取订单ID
    order_id_match = re.search(r'ORD\d+', cmd_input.upper())
    if order_id_match:
        params["order_id"] = order_id_match.group(0)

    # 提取新状态
    for status_key, status_cn in STATUS_MAP.items():
        if status_cn in cmd_input or status_key in cmd_input.lower():
            params["new_status"] = status_key
            break

    return params


if __name__ == "__main__":
    print("=" * 50)
    print("订单管理系统 - 命令行测试")
    print("=" * 50)

    # 测试所有功能
    print("\n>>> 1. 查询所有订单")
    result = handle_command("查询订单")
    print(result)

    print("\n>>> 2. 查询订单详情")
    result = handle_command("订单ORD20240115001的详细信息")
    print(result)

    print("\n>>> 3. 按待支付状态筛选")
    result = handle_command("查询待支付的订单")
    print(result)

    print("\n>>> 4. 订单统计")
    result = handle_command("统计二月份的订单情况")
    print(result)

    print("\n>>> 5. 创建订单")
    result = handle_command("创建一个新订单，客户李四，电话13800138002，蓝牙耳机 599 元")
    print(result)

    print("\n>>> 6. 更新订单状态")
    # 先用一个存在的订单
    result = handle_command("把订单ORD20240215001的状态改为已支付")
    print(result)
