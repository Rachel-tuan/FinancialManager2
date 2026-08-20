"""数据存储层：records.json / goals.json 的读写。

与原有 load_data/save_data/load_goals/save_goals 行为完全一致：
- 文件不存在时返回空值（[] / {}）
- UTF-8 编码，ensure_ascii=False，indent=2
- 仅做原始 JSON 结构的读写，不做模型转换
"""

import json
import os

from config import DATA_FILE, GOAL_FILE

DEFAULT_RECORDS_FILE = DATA_FILE
DEFAULT_GOALS_FILE = GOAL_FILE


def load_records(filepath=DEFAULT_RECORDS_FILE):
    """读取全部账单记录；文件不存在时返回空列表。"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_records(records, filepath=DEFAULT_RECORDS_FILE):
    """保存全部账单记录。"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_goals(filepath=DEFAULT_GOALS_FILE):
    """读取月度目标；文件不存在时返回空字典。"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_goals(goals, filepath=DEFAULT_GOALS_FILE):
    """保存月度目标。"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)