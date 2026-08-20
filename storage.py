"""数据存储层：records.json / goals.json 的读写。

与原有 load_data/save_data/load_goals/save_goals 行为完全一致：
- 文件不存在时返回空值（[] / {}）
- UTF-8 编码，ensure_ascii=False，indent=2
- 仅做原始 JSON 结构的读写，不做模型转换
"""

import json
import os

from config import DATA_FILE, GOAL_FILE
from exceptions import StorageError

DEFAULT_RECORDS_FILE = DATA_FILE
DEFAULT_GOALS_FILE = GOAL_FILE


def load_records(filepath=DEFAULT_RECORDS_FILE):
    """读取全部账单记录；文件不存在时返回空列表。

    文件读取或 JSON 解析失败时抛出 StorageError。
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except (OSError, ValueError) as e:
        raise StorageError(f'读取记录文件失败: {e}') from e


def save_records(records, filepath=DEFAULT_RECORDS_FILE):
    """保存全部账单记录。

    文件写入失败时抛出 StorageError。
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise StorageError(f'保存记录文件失败: {e}') from e


def load_goals(filepath=DEFAULT_GOALS_FILE):
    """读取月度目标；文件不存在时返回空字典。

    文件读取或 JSON 解析失败时抛出 StorageError。
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except (OSError, ValueError) as e:
        raise StorageError(f'读取目标文件失败: {e}') from e


def save_goals(goals, filepath=DEFAULT_GOALS_FILE):
    """保存月度目标。

    文件写入失败时抛出 StorageError。
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(goals, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise StorageError(f'保存目标文件失败: {e}') from e