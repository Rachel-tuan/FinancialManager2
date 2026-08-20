"""控制层：具体业务操作的编排逻辑。

接收 UI 传来的原始输入，内部完成校验、模型转换与持久化，
以 (是否成功, 提示信息) 返回结果；UI 只负责展示。
"""

from models import Record, Category, Goals
from storage import load_records, save_records, load_goals, save_goals
from services import monthly_totals, monthly_goal


def add_record(date, category, amount_str, note):
    """新增一条账单记录。

    :param date: 日期字符串（YYYY-MM-DD），不做清洗
    :param category: 分类字符串（收入/支出）
    :param amount_str: 金额原始输入字符串，内部完成清洗与校验
    :param note: 用途/备注
    :return: (是否成功, 提示信息)；失败时不写入任何数据
    """
    amount_str = amount_str.strip()
    note = note.strip()

    if not amount_str or not category:
        return False, '类型和金额不能为空！'

    try:
        amount = float(amount_str)
    except ValueError:
        return False, '金额必须是数字！'

    if amount <= 0:
        return False, '金额必须为正数！'

    amount = abs(amount)

    record = Record(date=date, category=Category.from_value(category),
                    amount=amount, note=note)
    data = load_records()
    data.append(record.to_dict())
    save_records(data)
    return True, '账单已添加！'


def set_goal(month, amount_str):
    """设置指定月份的目标金额。

    :param month: 月份原始输入字符串（YYYY-MM），内部做清洗
    :param amount_str: 目标金额原始输入字符串，内部完成清洗与校验
    :return: (是否成功, 提示信息)；失败时不写入任何数据
    """
    month = month.strip()
    amount_str = amount_str.strip()

    if not month or not amount_str:
        return False, '月份和目标金额不能为空！'

    try:
        amount = float(amount_str)
    except ValueError:
        return False, '目标金额必须是数字！'

    if amount <= 0:
        return False, '目标金额必须为正数！'

    goals = Goals.from_dict(load_goals())
    goals.set(month, amount)
    save_goals(goals.to_dict())
    return True, f'{month} 月支出目标已设置为 {amount:.2f}！'


def get_monthly_summary(month):
    """获取指定月份的月度统计摘要。

    :param month: 月份字符串（YYYY-MM）
    :return: dict，包含 month / income / expense / balance；
        goal 为 services.GoalStatus 对象（未设置目标时为 None）
    """
    records = load_records()
    income, expense, balance = monthly_totals(records, month)
    goals = load_goals()
    return {
        'month': month,
        'income': income,
        'expense': expense,
        'balance': balance,
        'goal': monthly_goal(goals, month, expense),
    }


def get_monthly_records(month):
    """获取指定月份的账单记录列表（按月份过滤）。

    :param month: 月份字符串（YYYY-MM）
    :return: 该月账单记录列表（保持 JSON 中的原始字典结构）
    """
    return [r for r in load_records() if r['date'].startswith(month)]


def get_usage_breakdown(month):
    """统计指定月份的支出用途分布。

    :param month: 月份字符串（YYYY-MM）
    :return: dict {用途/备注: 支出金额合计}，仅统计支出记录
    """
    usage = {}
    for r in load_records():
        if r['category'] == Category.EXPENSE.value and r['date'].startswith(month):
            usage[r['note']] = usage.get(r['note'], 0) + r['amount']
    return usage