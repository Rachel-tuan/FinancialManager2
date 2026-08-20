"""controller 层测试：add_record / set_goal / get_monthly_summary / get_monthly_records / get_usage_breakdown。"""

import json
import os

import pytest

import storage
from controller import (add_record, set_goal, get_monthly_summary,
                        get_monthly_records, get_usage_breakdown)
from exceptions import ValidationError
from services import monthly_totals, monthly_goal

ADD_CASES = [
    ('2026-08-01', '收入', '8000', '工资'),
    ('2026-08-03', '支出', '1500.5', '房租'),
    ('2026-08-10', '支出', ' 200.25 ', ' 餐饮 '),   # 带空格输入
    ('2026-08-15', '支出', '50', ''),                # 空备注
    ('2026-08-20', '收入', 'abc', '兼职'),           # 非数字
    ('2026-08-21', '收入', '', '备注'),              # 空金额
    ('2026-08-22', '支出', '-5', '负金额'),          # 非正数
    ('2026-08-23', '支出', '0', '零'),               # 零
]

GOAL_CASES = [
    ('2026-08', '2500'),
    ('2026-08', ' 3000 '),
    (' 2026-07 ', '1000'),
    ('2026-09', ''),
    ('', '100'),
    ('2026-10', 'abc'),
    ('2026-11', '0'),
    ('2026-12', '-5'),
]

SUMMARY_RECORDS = [
    {'date': '2026-08-01', 'category': '收入', 'amount': 8000.0, 'note': '工资'},
    {'date': '2026-08-03', 'category': '支出', 'amount': 1500.5, 'note': '房租'},
    {'date': '2026-08-10', 'category': '支出', 'amount': 200.25, 'note': '餐饮'},
    {'date': '2026-08-15', 'category': '支出', 'amount': 50.25, 'note': '交通'},
    {'date': '2026-07-30', 'category': '支出', 'amount': 999.0, 'note': '上月'},
    {'date': '2026-08-20', 'category': '收入', 'amount': 500.0, 'note': '兼职'},
]

USAGE_RECORDS = [
    {'date': '2026-08-01', 'category': '收入', 'amount': 8000.0, 'note': '工资'},
    {'date': '2026-08-03', 'category': '支出', 'amount': 1500.5, 'note': '房租'},
    {'date': '2026-08-10', 'category': '支出', 'amount': 200.25, 'note': '餐饮'},
    {'date': '2026-08-15', 'category': '支出', 'amount': 50.25, 'note': '交通'},
    {'date': '2026-08-05', 'category': '支出', 'amount': 300.0, 'note': '餐饮'},
    {'date': '2026-07-30', 'category': '支出', 'amount': 999.0, 'note': '上月'},
    {'date': '2026-07-31', 'category': '收入', 'amount': 100.0, 'note': '杂'},
]


def _write_json(filename, obj):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


# ---------- add_record ----------

def test_add_record_cases_match_old_behavior(data_dir):
    # 旧实现（v0.10.0 之前）的返回值语义，用于校验消息文本与写入行为
    expected = {
        ('2026-08-01', '收入', '8000', '工资'): (True, '账单已添加！'),
        ('2026-08-03', '支出', '1500.5', '房租'): (True, '账单已添加！'),
        ('2026-08-10', '支出', ' 200.25 ', ' 餐饮 '): (True, '账单已添加！'),
        ('2026-08-15', '支出', '50', ''): (True, '账单已添加！'),
        ('2026-08-20', '收入', 'abc', '兼职'): '金额必须是数字！',
        ('2026-08-21', '收入', '', '备注'): '类型和金额不能为空！',
        ('2026-08-22', '支出', '-5', '负金额'): '金额必须为正数！',
        ('2026-08-23', '支出', '0', '零'): '金额必须为正数！',
    }
    for i, (date, cat, amt, note) in enumerate(ADD_CASES):
        before = storage.load_records()
        result = expected[(date, cat, amt, note)]
        if isinstance(result, tuple):
            exp_ok, exp_msg = result
            ok, msg = add_record(date, cat, amt, note)
            assert ok == exp_ok, f"case{i}: ok 不一致 {ok} vs {exp_ok}"
            assert msg == exp_msg, f"case{i}: msg 不一致 {msg!r} vs {exp_msg!r}"
            new_file = storage.load_records()
            old_data = [dict(r) for r in before]
            old_data.append({'date': date, 'category': cat, 'amount': float(amt.strip()), 'note': note.strip()})
            assert new_file == old_data, f"case{i}: 写入内容与旧实现不一致"
            raw = open(storage.DEFAULT_RECORDS_FILE, 'rb').read()
            expected_bytes = json.dumps(old_data, ensure_ascii=False, indent=2).encode('utf-8')
            assert raw == expected_bytes, f"case{i}: 文件字节格式不一致"
        else:
            with pytest.raises(ValidationError) as ei:
                add_record(date, cat, amt, note)
            assert str(ei.value) == result, f"case{i}: 提示文字不一致 {str(ei.value)!r} vs {result!r}"
            assert storage.load_records() == before, f"case{i}: 校验失败却写入了数据"


def test_add_record_accumulates(data_dir):
    before_count = len(storage.load_records())
    add_record('2026-09-01', '支出', '100', '连续')
    add_record('2026-09-02', '支出', '200', '连续')
    assert len(storage.load_records()) == before_count + 2, "连续添加未累计"


def test_add_record_invalid_category_raises(data_dir):
    with pytest.raises(ValidationError) as ei:
        add_record('2026-09-03', '其他', '100', 'x')
    assert '无效的账单分类' in str(ei.value), f"提示文字不符: {str(ei.value)}"


# ---------- set_goal ----------

def test_set_goal_cases_match_old_behavior(data_dir):
    # 旧实现（v0.10.0 之前）的返回值语义，用于校验消息文本与写入行为
    expected = {
        ('2026-08', '2500'): (True, '2026-08 月支出目标已设置为 2500.00！'),
        ('2026-08', ' 3000 '): (True, '2026-08 月支出目标已设置为 3000.00！'),
        (' 2026-07 ', '1000'): (True, '2026-07 月支出目标已设置为 1000.00！'),
        ('2026-09', ''): '月份和目标金额不能为空！',
        ('', '100'): '月份和目标金额不能为空！',
        ('2026-10', 'abc'): '目标金额必须是数字！',
        ('2026-11', '0'): '目标金额必须为正数！',
        ('2026-12', '-5'): '目标金额必须为正数！',
    }
    for i, (month, amt) in enumerate(GOAL_CASES):
        before = storage.load_goals()
        result = expected[(month, amt)]
        if isinstance(result, tuple):
            exp_ok, exp_msg = result
            ok, msg = set_goal(month, amt)
            assert ok == exp_ok, f"case{i}: ok 不一致 {ok} vs {exp_ok}"
            assert msg == exp_msg, f"case{i}: msg 不一致 {msg!r} vs {exp_msg!r}"
            new_goals = storage.load_goals()
            old_goals = dict(before)
            old_goals[month.strip()] = float(amt.strip())
            assert new_goals == old_goals, f"case{i}: 写入内容与旧实现不一致"
            raw = open(storage.DEFAULT_GOALS_FILE, 'rb').read()
            expected_bytes = json.dumps(old_goals, ensure_ascii=False, indent=2).encode('utf-8')
            assert raw == expected_bytes, f"case{i}: 文件字节格式不一致"
        else:
            with pytest.raises(ValidationError) as ei:
                set_goal(month, amt)
            assert str(ei.value) == result, f"case{i}: 提示文字不一致 {str(ei.value)!r} vs {result!r}"
            assert storage.load_goals() == before, f"case{i}: 校验失败却写入了数据"


def test_set_goal_overwrites_existing(data_dir):
    set_goal('2026-08', '999')
    g = storage.load_goals()
    assert g['2026-08'] == 999.0, "覆盖已有目标失败"


# ---------- get_monthly_summary ----------

def test_summary_meets_goal(data_dir):
    _write_json('records.json', SUMMARY_RECORDS)
    _write_json('goals.json', {'2026-08': 2500})
    s = get_monthly_summary('2026-08')
    income, expense, balance = monthly_totals(SUMMARY_RECORDS, '2026-08')
    assert s['month'] == '2026-08', "月份字段错误"
    assert (s['income'], s['expense'], s['balance']) == (income, expense, balance), "摘要统计错误"
    assert s['goal'] is not None and s['goal'].status == '达标', "达标状态错误"


def test_summary_no_goal_month(data_dir):
    _write_json('records.json', SUMMARY_RECORDS)
    _write_json('goals.json', {'2026-08': 2500})
    s = get_monthly_summary('2026-07')
    assert s['goal'] is None, "未设置目标的月份应返回 None"


def test_summary_empty_month(data_dir):
    _write_json('records.json', SUMMARY_RECORDS)
    _write_json('goals.json', {'2026-08': 2500})
    s = get_monthly_summary('2026-01')
    assert (s['income'], s['expense'], s['balance']) == (0, 0, 0), "空月份统计错误"
    assert s['goal'] is None, "空月份目标应为 None"


def test_summary_over_budget(data_dir):
    _write_json('records.json', SUMMARY_RECORDS)
    _write_json('goals.json', {'2026-08': 100})
    s = get_monthly_summary('2026-08')
    assert s['goal'].status == '超支', "超支状态错误"


def test_summary_no_data_files(data_dir):
    s = get_monthly_summary('2026-08')
    assert (s['income'], s['expense'], s['balance']) == (0, 0, 0), "无数据文件统计错误"
    assert s['goal'] is None, "无数据文件目标应为 None"


def test_summary_equivalent_old_chain(data_dir):
    _write_json('records.json', SUMMARY_RECORDS)
    _write_json('goals.json', {'2026-08': 2500})
    for m in ['2026-08', '2026-07', '2026-01']:
        old_inc, old_exp, old_bal = monthly_totals(storage.load_records(), m)
        old_gi = monthly_goal(storage.load_goals(), m, old_exp)
        new = get_monthly_summary(m)
        assert (new['income'], new['expense'], new['balance']) == (old_inc, old_exp, old_bal), \
            f"与旧调用链不一致: month={m}"
        assert (new['goal'] is None) == (old_gi is None), f"goal 存在性不一致: month={m}"
        if old_gi is not None:
            assert (new['goal'].goal, new['goal'].remaining, new['goal'].status) == \
                (old_gi.goal, old_gi.remaining, old_gi.status), f"goal 内容不一致: month={m}"


# ---------- get_monthly_records / get_usage_breakdown ----------

def old_monthly_records(data, month):
    return [r for r in data if r['date'].startswith(month)]


def old_usage_breakdown(data, month):
    usage = {}
    for r in data:
        if r['category'] == '支出' and r['date'].startswith(month):
            usage[r['note']] = usage.get(r['note'], 0) + r['amount']
    return usage


def test_get_monthly_records_equivalence(data_dir):
    _write_json('records.json', USAGE_RECORDS)
    for m in ['2026-08', '2026-07', '2026-01', '']:
        new = get_monthly_records(m)
        old = old_monthly_records(USAGE_RECORDS, m)
        assert new == old, f"records 与旧过滤逻辑不一致: month={m!r}"


def test_get_monthly_records_key_structure(data_dir):
    _write_json('records.json', USAGE_RECORDS)
    for r in get_monthly_records('2026-08'):
        assert list(r.keys()) == ['date', 'category', 'amount', 'note'], "键结构被改变"


def test_get_usage_breakdown_equivalence(data_dir):
    _write_json('records.json', USAGE_RECORDS)
    for m in ['2026-08', '2026-07', '2026-01']:
        new = get_usage_breakdown(m)
        old = old_usage_breakdown(USAGE_RECORDS, m)
        assert new == old, f"usage 与旧聚合逻辑不一致: month={m}"


def test_usage_breakdown_aggregates_same_note(data_dir):
    _write_json('records.json', USAGE_RECORDS)
    assert get_usage_breakdown('2026-08')['餐饮'] == 200.25 + 300.0, "同用途未累加"


def test_usage_breakdown_excludes_income(data_dir):
    _write_json('records.json', USAGE_RECORDS)
    assert '工资' not in get_usage_breakdown('2026-08'), "收入被计入支出分布"


def test_records_and_usage_missing_file(data_dir):
    assert get_monthly_records('2026-08') == [], "无数据文件 records 应为空"
    assert get_usage_breakdown('2026-08') == {}, "无数据文件 usage 应为空"


def test_ui_consumption_path(data_dir):
    _write_json('records.json', USAGE_RECORDS)
    rows = sorted(get_monthly_records('2026-08'), key=lambda x: x['date'], reverse=True)
    assert rows[0]['date'] >= rows[-1]['date'], "排序示例失败"
    usage = get_usage_breakdown('2026-08')
    total = sum(usage.values())
    expected = 1500.5 + 200.25 + 50.25 + 300.0
    assert abs(total - expected) < 1e-9, "图表总额不符"