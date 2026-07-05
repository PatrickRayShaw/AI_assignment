"""
Chat Agent - 智能订单管理助手
通过自然语言理解用户意图，自动匹配并调用订单管理技能。

支持功能：
1. 订单查询（多条件筛选、分页）
2. 订单详情查看
3. 订单创建
4. 订单状态更新
5. 订单统计分析
"""

import json
import os
import re
from datetime import datetime, timedelta
from order_manager import OrderManager

class ChatAgent:
    def __init__(self):
        self.manager = OrderManager()
        self.skills = self.load_skills()
        self.conversation_history = []

    def load_skills(self):
        """从 skills/SKILL.md 加载技能定义"""
        skills = {
            "list_orders": {
                "name": "订单查询",
                "keywords": [
                    "查询订单", "查看订单", "订单列表", "最近订单", "我的订单",
                    "查订单", "查单", "订单在哪", "下了什么单", "有什么订单",
                    "list orders", "show orders", "get orders", "all orders",
                    "查询", "看看订单", "看下订单",
                ],
                "params": ["status", "start_date", "end_date", "customer_name", "page", "page_size"],
            },
            "get_order_detail": {
                "name": "订单详情",
                "keywords": [
                    "订单详情", "订单信息", "查看订单", "订单明细", "详情",
                    "order detail", "order info", "get order",
                    "第.*个订单", "订单号.*", "ORD.*",
                ],
                "params": ["order_id"],
            },
            "create_order": {
                "name": "创建订单",
                "keywords": [
                    "创建订单", "新建订单", "下单", "新订单", "帮我创建", "帮我下单",
                    "create order", "new order", "place order",
                    "买", "购买", "订购",
                ],
                "params": ["customer_name", "phone", "amount", "items", "status"],
            },
            "update_order_status": {
                "name": "更新订单状态",
                "keywords": [
                    "更新订单", "修改订单", "订单状态", "更改状态", "修改状态",
                    "改为", "改成", "更新为", "标记为", "设为",
                    "update order", "change status", "set status",
                    "已支付", "发货", "完成", "取消",
                ],
                "params": ["order_id", "new_status"],
            },
            "order_statistics": {
                "name": "订单统计",
                "keywords": [
                    "统计订单", "订单统计", "订单汇总", "订单数据",
                    "order stats", "order statistics", "order summary",
                    "统计", "汇总", "一共", "总共", "总金额",
                    "几笔订单", "多少订单", "一个月.*订单",
                ],
                "params": ["start_date", "end_date", "group_by"],
            },
        }
        return skills

    def detect_intent(self, user_input: str):
        """识别用户意图，返回 (action, confidence)"""
        scores = {}
        for action, skill in self.skills.items():
            score = 0
            for keyword in skill["keywords"]:
                if re.search(keyword, user_input, re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[action] = score

        if not scores:
            return None, 0

        best_action = max(scores, key=scores.get)
        return best_action, scores[best_action]

    def extract_params(self, user_input: str, action: str):
        """从用户输入中提取参数"""
        params = {}

        # 提取订单ID（数字或ORD开头的编号）
        id_match = re.search(r'(?:订单|ORD)(\d+)', user_input, re.IGNORECASE)
        if not id_match:
            id_match = re.search(r'(?:第\s*)?(\d+)\s*(?:个|号)?\s*订单', user_input)
        if not id_match:
            id_match = re.search(r'(?:订单|id)[:：\s]*(\d+)', user_input, re.IGNORECASE)
        if id_match:
            params["order_id"] = int(id_match.group(1))

        # 提取状态
        status_map = {
            "待支付": "pending", "未支付": "pending", "pending": "pending",
            "已支付": "paid", "支付": "paid", "paid": "paid",
            "发货": "shipped", "已发货": "shipped", "配送中": "shipped", "shipped": "shipped",
            "已完成": "completed", "完成": "completed", "completed": "completed",
            "已取消": "cancelled", "取消": "cancelled", "cancelled": "cancelled",
        }
        for cn, en in status_map.items():
            if cn in user_input:
                params["status"] = en if action == "list_orders" else None
                if action == "update_order_status":
                    params["new_status"] = en
                break

        # 提取金额
        amount_match = re.search(r'(\d+(?:\.\d{1,2})?)\s*元', user_input)
        if amount_match:
            params["amount"] = float(amount_match.group(1))

        # 提取客户名称
        name_patterns = [
            r'客户[：:\s]*([\u4e00-\u9fa5]{2,4})',
            r'用户[：:\s]*([\u4e00-\u9fa5]{2,4})',
            r'给\s*([\u4e00-\u9fa5]{2,4})',
            r'([\u4e00-\u9fa5]{2,3})(?:买|订购|下单)',
        ]
        for pattern in name_patterns:
            m = re.search(pattern, user_input)
            if m:
                params["customer_name"] = m.group(1)
                break

        # 提取电话号码
        phone_match = re.search(r'1[3-9]\d{9}', user_input)
        if phone_match:
            params["phone"] = phone_match.group(0)

        # 提取日期范围
        date_patterns = [
            (r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', "exact"),
            (r'(一|1)月', lambda: ("2024-01-01", "2024-01-31")),
            (r'(二|2)月', lambda: ("2024-02-01", "2024-02-29")),
            (r'(三|3)月', lambda: ("2024-03-01", "2024-03-31")),
            (r'本月', lambda: (datetime.now().replace(day=1).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))),
        ]
        for pattern, handler in date_patterns:
            if isinstance(handler, str) and handler == "exact":
                dates = re.findall(pattern, user_input)
                if len(dates) >= 2:
                    params["start_date"] = dates[0].replace("/", "-")
                    params["end_date"] = dates[1].replace("/", "-")
                elif len(dates) == 1:
                    params["start_date"] = dates[0].replace("/", "-")
            elif callable(handler):
                if re.search(pattern, user_input):
                    sd, ed = handler()
                    params["start_date"] = sd
                    params["end_date"] = ed

        # 提取分页参数
        page_match = re.search(r'第\s*(\d+)\s*页', user_input)
        if page_match:
            params["page"] = int(page_match.group(1))

        # 提取商品信息
        item_match = re.search(r'买(?:了|一个|个)?(.+?)(?:,|，|$)', user_input)
        if item_match and action == "create_order":
            item_name = item_match.group(1).strip()
            if item_name and not item_name.startswith(("订单", "客户")):
                params["items"] = [{"name": item_name, "price": params.get("amount", 0), "quantity": 1}]

        # 提取 group_by
        if "按月" in user_input or "月份" in user_input:
            params["group_by"] = "month"
        elif "分类" in user_input or "类别" in user_input:
            params["group_by"] = "category"
        else:
            params["group_by"] = "status"

        return params

    def format_response(self, action: str, result: dict) -> str:
        """将执行结果格式化为自然语言"""
        if not result.get("success"):
            return f"❌ 操作失败：{result.get('error', '未知错误')}"

        data = result.get("data", {})

        if action == "list_orders":
            orders = data.get("orders", [])
            total = data.get("total", 0)
            if not orders:
                return "📋 暂无订单记录。"
            lines = [f"📋 找到 {total} 个订单（第{data.get('page',1)}/{data.get('total_pages',1)}页）："]
            for o in orders:
                status_cn = {"pending":"待支付","paid":"已支付","shipped":"发货中","completed":"已完成","cancelled":"已取消"}.get(o["status"], o["status"])
                lines.append(f"  • {o['order_number']} - {o['customer_name']} - ¥{o['amount']:.2f} - {status_cn}")
            return "\n".join(lines)

        elif action == "get_order_detail":
            o = data
            status_cn = {"pending":"待支付","paid":"已支付","shipped":"发货中","completed":"已完成","cancelled":"已取消"}.get(o["status"], o["status"])
            lines = [
                f"📦 订单 {o['order_number']} 详细信息：",
                f"  客户：{o['customer_name']}",
                f"  电话：{o['phone']}",
                f"  金额：¥{o['amount']:.2f}",
                f"  状态：{status_cn}",
                f"  日期：{o['create_time']}",
            ]
            items = o.get("items", [])
            if items:
                lines.append(f"  商品明细：")
                for item in items:
                    lines.append(f"    - {item['name']} x{item.get('quantity',1)} = ¥{item.get('price',0):.2f}")
            return "\n".join(lines)

        elif action == "create_order":
            o = data
            return f"✅ 订单创建成功！\n  订单号：{o['order_number']}\n  客户：{o['customer_name']}\n  金额：¥{o['amount']:.2f}"

        elif action == "update_order_status":
            status_cn = {"pending":"待支付","paid":"已支付","shipped":"发货中","completed":"已完成","cancelled":"已取消"}
            old_cn = status_cn.get(data.get("old_status",""), data.get("old_status",""))
            new_cn = status_cn.get(data.get("new_status",""), data.get("new_status",""))
            return f"✅ {data.get('message', f'订单状态已更新：{old_cn} → {new_cn}')}"

        elif action == "order_statistics":
            lines = [
                f"📊 订单统计：",
                f"  总订单数：{data['total_orders']} 笔",
                f"  总金额：¥{data['total_amount']:.2f}",
                f"  平均金额：¥{data['average_amount']:.2f}",
            ]
            if "by_status" in data:
                lines.append("  按状态分布：")
                status_cn = {"pending":"待支付","paid":"已支付","shipped":"发货中","completed":"已完成","cancelled":"已取消"}
                for st, info in data["by_status"].items():
                    lines.append(f"    {status_cn.get(st, st)}：{info['count']}笔 / ¥{info['total_amount']:.2f}")
            if "by_month" in data:
                lines.append("  按月份分布：")
                for month, info in sorted(data["by_month"].items()):
                    lines.append(f"    {month}：{info['count']}笔 / ¥{info['total_amount']:.2f}")
            if "by_category" in data:
                lines.append("  按类别分布：")
                for cat, info in data["by_category"].items():
                    lines.append(f"    {cat}：{info['count']}件 / ¥{info['total_amount']:.2f}")
            return "\n".join(lines)

        return json.dumps(result, ensure_ascii=False, indent=2)

    def execute_action(self, action: str, params: dict) -> dict:
        """执行对应的技能操作"""
        if action == "list_orders":
            return self.manager.list_orders(
                page=params.get("page", 1),
                page_size=params.get("page_size", 10),
                status=params.get("status"),
                start_date=params.get("start_date"),
                end_date=params.get("end_date"),
                customer_name=params.get("customer_name"),
            )
        elif action == "get_order_detail":
            oid = params.get("order_id")
            if not oid:
                return {"success": False, "error": "请指定订单ID或编号"}
            return self.manager.get_order_detail(oid)
        elif action == "create_order":
            required = ["customer_name", "phone", "amount"]
            for r in required:
                if r not in params:
                    return {"success": False, "error": f"缺少必要参数: {r}"}
            return self.manager.create_order(
                customer_name=params["customer_name"],
                phone=params["phone"],
                amount=params["amount"],
                items=params.get("items", []),
                status=params.get("status", "pending"),
            )
        elif action == "update_order_status":
            oid = params.get("order_id")
            new_status = params.get("new_status")
            if not oid:
                return {"success": False, "error": "请指定要更新的订单ID"}
            if not new_status:
                return {"success": False, "error": "请指定新状态"}
            return self.manager.update_order_status(oid, new_status)
        elif action == "order_statistics":
            return self.manager.order_statistics(
                start_date=params.get("start_date"),
                end_date=params.get("end_date"),
                group_by=params.get("group_by", "status"),
            )
        return {"success": False, "error": f"未知操作: {action}"}

    def process(self, user_input: str) -> str:
        """核心处理流程：意图识别 → 参数提取 → 执行 → 格式化"""
        self.conversation_history.append({"role": "user", "content": user_input})

        # Step 1: 意图识别
        action, confidence = self.detect_intent(user_input)
        if not action:
            return (
                "🤔 抱歉，我没有理解您的意图。\n"
                "您可以尝试以下表达：\n"
                "  • 查询订单 / 查看最近的订单\n"
                "  • 查看订单1的详情\n"
                "  • 创建订单，客户王五，电话13800138003，购买机械键盘1299元\n"
                "  • 把订单2改为已支付\n"
                "  • 统计二月份的订单"
            )

        # Step 2: 参数提取
        params = self.extract_params(user_input, action)

        # Step 3: 执行
        result = self.execute_action(action, params)

        # Step 4: 格式化响应
        response = self.format_response(action, result)

        self.conversation_history.append({"role": "agent", "content": response})
        return response

    def run(self):
        """启动交互式对话"""
        print("=" * 60)
        print("🤖 订单管理 Chat Agent 已就绪")
        print("   支持：查询订单 | 查看详情 | 创建订单 | 更新状态 | 统计分析")
        print("   输入 /exit 退出, /help 查看帮助")
        print("=" * 60)
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() == "/exit":
                    print("👋 再见！")
                    break
                if user_input.lower() == "/help":
                    print("\n📖 使用示例：")
                    print("  • 查询最近的订单")
                    print("  • 查看订单1的详情")
                    print("  • 查询已支付的订单")
                    print("  • 创建订单，客户王五，电话13800138003，购买机械键盘1299元")
                    print("  • 把订单2改为已支付")
                    print("  • 统计二月份的订单")
                    continue
                if not user_input:
                    continue
                response = self.process(user_input)
                print(f"\nAgent: {response}")
            except (EOFError, KeyboardInterrupt):
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"\n⚠️ 出错了：{e}")

if __name__ == "__main__":
    agent = ChatAgent()
    agent.run()
