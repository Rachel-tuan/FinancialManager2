import json
import os

from config import DATA_FILE, GOAL_FILE
from exceptions import StorageError
from logger import logger

DEFAULT_RECORDS_FILE = DATA_FILE
DEFAULT_GOALS_FILE = GOAL_FILE


def load_records(filepath=DEFAULT_RECORDS_FILE):
    """读取全部账单记录；文件不存在时返回空列表。

    文件读取或 JSON 解析失败时抛出 StorageError。
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.debug(f'读取记录文件: {filepath}（{len(data)} 条）')
            return data
        logger.debug(f'记录文件不存在，返回空列表: {filepath}')
        return []
    except (OSError, ValueError) as e:
        logger.error(f'读取记录文件失败: {filepath} - {e}')
        raise StorageError(f'读取记录文件失败: {e}') from e


def save_records(records, filepath=DEFAULT_RECORDS_FILE):
    """保存全部账单记录。

    文件写入失败时抛出 StorageError。
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        logger.debug(f'保存记录文件: {filepath}（{len(records)} 条）')
    except OSError as e:
        logger.error(f'保存记录文件失败: {filepath} - {e}')
        raise StorageError(f'保存记录文件失败: {e}') from e


def load_goals(filepath=DEFAULT_GOALS_FILE):
    """读取月度目标；文件不存在时返回空字典。

    文件读取或 JSON 解析失败时抛出 StorageError。
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.debug(f'读取目标文件: {filepath}（{len(data)} 个）')
            return data
        logger.debug(f'目标文件不存在，返回空字典: {filepath}')
        return {}
    except (OSError, ValueError) as e:
        logger.error(f'读取目标文件失败: {filepath} - {e}')
        raise StorageError(f'读取目标文件失败: {e}') from e


def save_goals(goals, filepath=DEFAULT_GOALS_FILE):
    """保存月度目标。

    文件写入失败时抛出 StorageError。
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(goals, f, ensure_ascii=False, indent=2)
        logger.debug(f'保存目标文件: {filepath}（{len(goals)} 个）')
    except OSError as e:
        logger.error(f'保存目标文件失败: {filepath} - {e}')
        raise StorageError(f'保存目标文件失败: {e}') from e