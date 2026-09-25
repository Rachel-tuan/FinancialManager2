"""models 层测试：JSON 往返、Category 映射、边界输入。"""

import json

import pytest

from models import Category, Record, Goals
from services import monthly_totals, monthly_goal

RECORDS_JSON = [
    {'date': '2026-08-01', 'category': '收入', 'amount': 8000.0, 'note': '工资'},
    {'date': '2026-08-03', 'category': '支出', 'amount': 1500.5, 'note': '房租'},
    {'date': '2026-08-10', 'category': '支出', 'amount': 200.25, 'note': '餐饮'},
]
GOALS_JSON = {'2026-08': 2500, '2026-07': 1000}


def _dump(o):
    return json.dumps(o, ensure_ascii=False, indent=2)


def test_json_roundtrip_keeps_raw_dict():
    records = [Record.from_dict(d) for d in RECORDS_JSON]
    for model, raw in zip(records, RECORDS_JSON):
        assert model.to_dict() == raw, f"to_dict 与原始字典不一致: {model.to_dict()} vs {raw}"
        assert list(model.to_dict().keys()) == ['date', 'category', 'amount', 'note'], "键顺序被改变"


def test_goals_roundtrip():
    goals = Goals.from_dict(GOALS_JSON)
    assert goals.to_dict() == GOALS_JSON, f"goals 往返不一致: {goals.to_dict()}"


def test_full_chain_dump_equal():
    records = [Record.from_dict(d) for d in RECORDS_JSON]
    assert _dump([r.to_dict() for r in records]) == _dump(RECORDS_JSON), "records 全链路输出不一致"
    assert _dump(Goals.from_dict(GOALS_JSON).to_dict()) == _dump(GOALS_JSON), "goals 全链路输出不一致"


def test_category_enum_values():
    assert Category.INCOME.value == '收入', "Category.INCOME 值错误"
    assert Category.EXPENSE.value == '支出', "Category.EXPENSE 值错误"


def test_services_compat():
    records = [Record.from_dict(d) for d in RECORDS_JSON]
    income, expense, balance = monthly_totals([r.to_dict() for r in records], '2026-08')
    assert income == 8000, f"收入统计错误: {income}"
    assert expense == 1700.75, f"支出统计错误: {expense}"
    assert balance == 6299.25, f"结余统计错误: {balance}"
    gi = monthly_goal(GOALS_JSON, '2026-08', expense)
    assert gi is not None, "2026-08 应存在目标"
    assert gi.goal == 2500 and gi.remaining == 799.25, f"目标信息错误: {gi}"


def test_edge_inputs():
    assert Record.from_dict({'date': '2026-08-01', 'category': '支出', 'amount': 1, 'note': ''}).note == ''
    assert Goals.from_dict({}).to_dict() == {}, "空 Goals 往返应保持为空"
    goals = Goals.from_dict(GOALS_JSON)
    assert goals.get('2026-01') is None, "未设置月份应返回 None"
    goals.set('2026-09', 3000)
    assert goals.get('2026-09') == 3000, "set 后读取不一致"


def test_invalid_category_raises():
    with pytest.raises(ValueError):
        Record.from_dict({'date': '2026-08-01', 'category': '其他', 'amount': 1, 'note': ''})