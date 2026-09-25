"""业务逻辑层：月度统计相关纯函数。

仅依赖标准库，不依赖 UI（tkinter）与数据存储（JSON 文件），
便于单元测试与后续拆分。
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

from config import INCOME, EXPENSE

INCOME_CATEGORY = INCOME
EXPENSE_CATEGORY = EXPENSE


def monthly_totals(records, month):
    """计算指定月份的收入、支出与结余。

    :param records: 账单记录列表，元素为 dict:
        {'date': 'YYYY-MM-DD', 'category': '收入'/'支出', 'amount': 数字, 'note': str}
    :param month: 月份字符串，如 '2026-08'
    :return: (income, expense, balance)，均为 Decimal
    """
    income = sum(
        (Decimal(str(r['amount'])) for r in records
         if r['category'] == INCOME_CATEGORY and r['date'].startswith(month)),
        Decimal('0'),
    )
    expense = sum(
        (Decimal(str(r['amount'])) for r in records
         if r['category'] == EXPENSE_CATEGORY and r['date'].startswith(month)),
        Decimal('0'),
    )
    return income, expense, income - expense


@dataclass
class GoalStatus:
    """月度支出目标信息。"""

    goal: Decimal
    remaining: Decimal
    status: str


def monthly_goal(goals, month, expense):
    """查询指定月份的目标信息；未设置目标时返回 None。

    :param goals: 月度目标字典 {月份: 金额}
    :param month: 月份字符串，如 '2026-08'
    :param expense: 该月支出（Decimal）
    """
    if month not in goals:
        return None
    goal = Decimal(str(goals[month]))
    remaining = goal - expense
    return GoalStatus(goal=goal, remaining=remaining,
                      status='达标' if remaining >= 0 else '超支')


def format_decimal(value):
    """格式化为保留两位小数的 Decimal（四舍五入）。"""
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)