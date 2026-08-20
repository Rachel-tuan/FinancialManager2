"""控制层：具体业务操作的编排逻辑。

接收 UI 传来的原始输入，内部完成校验、模型转换与持久化，
以 (是否成功, 提示信息) 返回结果；UI 只负责展示。
"""

from models import Record, Category
from storage import load_records, save_records


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