"""view_models 层测试：表格行 / 图表数据构建。"""

import re
import inspect

from storage import save_records, save_goals
from controller import get_monthly_records, get_usage_breakdown
from view_models import build_table_rows, build_expense_chart_data

RECORDS = [
    {'date': '2026-08-01', 'category': '支出', 'amount': 1500.5, 'note': '房租'},
    {'date': '2026-08-03', 'category': '收入', 'amount': 8000.0, 'note': '工资'},
    {'date': '2026-08-02', 'category': '支出', 'amount': 45.5, 'note': '餐饮'},
    {'date': '2026-08-02', 'category': '支出', 'amount': 45.5, 'note': '餐饮'},
    {'date': '2026-07-31', 'category': '支出', 'amount': 99.0, 'note': '上月'},
    {'date': '2026-08-01', 'category': '收入', 'amount': 200.25, 'note': '红包'},
]
GOALS = {'2026-08': 3000.0}


def _seed(data_dir):
    save_records(RECORDS)
    save_goals(GOALS)


def old_table(month):
    sorted_data = sorted(get_monthly_records(month), key=lambda x: x['date'], reverse=True)
    rows = []
    for r in sorted_data:
        amount = r['amount']
        if r['category'] == '支出':
            amount_str = f"-{amount:.2f}"
        else:
            amount_str = f"+{amount:.2f}"
        rows.append({'date': r['date'], 'category': r['category'], 'amount': amount_str, 'note': r['note']})
    return rows


def old_chart(month):
    usage = get_usage_breakdown(month)
    sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
    return {'labels': [i[0] for i in sorted_usage], 'values': [i[1] for i in sorted_usage]}


def test_table_rows_equivalent_to_old(data_dir):
    _seed(data_dir)
    assert build_table_rows('2026-08') == old_table('2026-08'), "表格数据与旧逻辑不等价"


def test_table_rows_sorted_and_formatted(data_dir):
    _seed(data_dir)
    rows = build_table_rows('2026-08')
    assert rows[0]['date'] == '2026-08-03' and rows[0]['amount'] == '+8000.00', "降序排序或收入格式错误"
    assert rows[1]['amount'] == '-45.50', f"支出格式错误: {rows[1]}"
    assert len(rows) == 5, f"8月应为5条, 实际 {len(rows)}"
    dates = [r['date'] for r in rows]
    assert dates == sorted(dates, reverse=True), "非降序"


def test_table_rows_empty_month(data_dir):
    _seed(data_dir)
    assert build_table_rows('2026-01') == [], "空月份应返回空列表"


def test_chart_data_equivalent_to_old(data_dir):
    _seed(data_dir)
    assert build_expense_chart_data('2026-08') == old_chart('2026-08'), "图表数据与旧逻辑不等价"


def test_chart_data_sorted(data_dir):
    _seed(data_dir)
    cd = build_expense_chart_data('2026-08')
    assert cd['labels'] == ['房租', '餐饮'], f"标签错误: {cd['labels']}"
    assert cd['values'] == [1500.5, 91.0], f"values 错误: {cd['values']}"
    assert cd['values'] == sorted(cd['values'], reverse=True), "未按金额降序"


def test_chart_data_empty_month(data_dir):
    _seed(data_dir)
    assert build_expense_chart_data('2026-01') == {'labels': [], 'values': []}, "空月份图表数据错误"


def test_no_tkinter_matplotlib_imports():
    src = inspect.getsource(__import__('view_models'))
    for line in src.splitlines():
        if re.match(r'\s*(import|from)\s', line):
            assert 'tkinter' not in line and 'matplotlib' not in line, f"意外依赖: {line}"