"""storage 层测试：文件读写、JSON 格式兼容。"""

import json

import storage

RECORDS = [
    {'date': '2026-08-01', 'category': '收入', 'amount': 8000.0, 'note': '工资'},
    {'date': '2026-08-03', 'category': '支出', 'amount': 1500.5, 'note': '房租'},
    {'date': '2026-08-10', 'category': '支出', 'amount': 200.25, 'note': '餐饮'},
]
GOALS = {'2026-08': 2500, '2026-07': 1000}


def test_missing_file_returns_empty(tmp_path):
    rp = str(tmp_path / 'records.json')
    gp = str(tmp_path / 'goals.json')
    assert storage.load_records(rp) == [], "文件不存在时应返回空列表"
    assert storage.load_goals(gp) == {}, "文件不存在时应返回空字典"


def test_save_load_roundtrip(tmp_path):
    rp = str(tmp_path / 'records.json')
    gp = str(tmp_path / 'goals.json')
    storage.save_records(RECORDS, rp)
    storage.save_goals(GOALS, gp)
    assert storage.load_records(rp) == RECORDS, "records 往返不一致"
    assert storage.load_goals(gp) == GOALS, "goals 往返不一致"


def test_file_format_bytes(tmp_path):
    rp = str(tmp_path / 'records.json')
    storage.save_records(RECORDS, rp)
    raw = open(rp, 'rb').read()
    assert raw.startswith(b'['), "records 非数组开头"
    assert '工资'.encode('utf-8') in raw, "中文未被原样保存（ensure_ascii 失效）"
    assert not raw.startswith(b'\xef\xbb\xbf'), "文件存在 BOM"
    expected = json.dumps(RECORDS, ensure_ascii=False, indent=2).encode('utf-8')
    assert raw == expected, "records 文件内容与预期不符"
    gp = str(tmp_path / 'goals.json')
    storage.save_goals(GOALS, gp)
    graw = open(gp, 'rb').read()
    assert graw == json.dumps(GOALS, ensure_ascii=False, indent=2).encode('utf-8'), "goals 文件内容与预期不符"


def test_default_paths():
    assert storage.DEFAULT_RECORDS_FILE == 'records.json', "默认记录文件名错误"
    assert storage.DEFAULT_GOALS_FILE == 'goals.json', "默认目标文件名错误"
    assert storage.load_records.__defaults__[0] == 'records.json', "load_records 默认参数错误"


def test_empty_data_save_load(tmp_path):
    rp = str(tmp_path / 'e.json')
    storage.save_records([], rp)
    assert storage.load_records(rp) == [], "空列表往返不一致"
    gp = str(tmp_path / 'eg.json')
    storage.save_goals({}, gp)
    assert storage.load_goals(gp) == {}, "空字典往返不一致"