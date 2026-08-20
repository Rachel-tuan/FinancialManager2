"""展示数据层（ViewModel）：为 UI 控件准备展示数据。

只做数据准备与格式转换，不操作 tkinter / matplotlib；
数据来源为 controller，输出结构直接供 Treeview / 图表消费。
"""

from controller import get_monthly_records, get_usage_breakdown


def build_table_rows(month):
    """构建账单表格展示行数据。

    :param month: 月份字符串（YYYY-MM）
    :return: 按日期降序排序的列表，元素为
        {'date': ..., 'category': ..., 'amount': 格式化金额字符串, 'note': ...}
    """
    rows = []
    for r in sorted(get_monthly_records(month), key=lambda x: x['date'], reverse=True):
        amount = r['amount']
        if r['category'] == '支出':
            amount_str = f"-{amount:.2f}"
        else:
            amount_str = f"+{amount:.2f}"
        rows.append({
            'date': r['date'],
            'category': r['category'],
            'amount': amount_str,
            'note': r['note'],
        })
    return rows


def build_expense_chart_data(month):
    """构建支出用途分布图表数据。

    :param month: 月份字符串（YYYY-MM）
    :return: {'labels': [用途...], 'values': [金额...]}，按金额从大到小排序
    """
    usage = get_usage_breakdown(month)
    sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
    return {
        'labels': [item[0] for item in sorted_usage],
        'values': [item[1] for item in sorted_usage],
    }