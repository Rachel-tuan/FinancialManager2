"""services 层测试：monthly_totals / monthly_goal 与旧实现等价。"""

from decimal import Decimal, ROUND_HALF_UP

from services import monthly_totals, monthly_goal, format_decimal

RECORDS = [
    {'date': '2026-08-01', 'category': '收入', 'amount': 8000, 'note': '工资'},
    {'date': '2026-08-03', 'category': '支出', 'amount': 1500.5, 'note': '房租'},
    {'date': '2026-08-10', 'category': '支出', 'amount': 200.25, 'note': '餐饮'},
    {'date': '2026-08-15', 'category': '支出', 'amount': 50.25, 'note': '交通'},
    {'date': '2026-07-30', 'category': '支出', 'amount': 999, 'note': '上月的'},
    {'date': '2026-08-20', 'category': '收入', 'amount': 500, 'note': '兼职'},
    {'date': '2026-08-05', 'category': '支出', 'amount': 300, 'note': '餐饮'},
]
GOALS = {'2026-08': 2500, '2026-07': 1000}

CASES = [
    (RECORDS, '2026-08'),
    (RECORDS, '2026-07'),
    (RECORDS, '2026-01'),
    ([], '2026-08'),
    ([r for r in RECORDS if r['category'] == '支出'], '2026-08'),
]


def old_totals(data, month):
    income = sum(Decimal(str(r['amount'])) for r in data
                 if r['category'] == '收入' and r['date'].startswith(month))
    expense = sum(Decimal(str(r['amount'])) for r in data
                  if r['category'] == '支出' and r['date'].startswith(month))
    return income, expense, income - expense


def old_goal(goals, month, expense):
    goal = goals.get(month, None)
    if goal is None:
        return None
    goal_dec = Decimal(str(goal))
    remaining = goal_dec - expense
    return goal_dec, remaining, "达标" if remaining >= 0 else "超支"


def test_monthly_totals_equivalence_with_old():
    for data, month in CASES:
        oi, oe, ob = old_totals(data, month)
        ni, ne, nb = monthly_totals(data, month)
        assert (oi, oe, ob) == (ni, ne, nb), f"totals 与旧实现不一致: month={month}"


def test_monthly_goal_equivalence_with_old():
    for data, month in CASES:
        _, oe, _ = old_totals(data, month)
        ne = monthly_totals(data, month)[1]
        og = old_goal(GOALS, month, oe)
        ng = monthly_goal(GOALS, month, ne)
        if og is None:
            assert ng is None, f"goal 应为 None: month={month}"
        else:
            assert (og[0], og[1], og[2]) == (ng.goal, ng.remaining, ng.status), \
                f"goal 与旧实现不一致: month={month}"


def test_format_decimal_equivalence_with_old():
    for data, month in CASES:
        _, oe, _ = old_totals(data, month)
        ne = monthly_totals(data, month)[1]
        expected = Decimal(str(oe)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        assert format_decimal(ne) == expected, f"format_decimal 不一致: month={month}"


def test_format_decimal_zero():
    assert format_decimal(Decimal('0')) == Decimal('0.00'), "零值格式化错误"