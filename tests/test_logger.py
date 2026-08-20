"""logger 层测试：统一日志实例、格式与文件输出。

同时验证 v0.10.0 的异常行为在接入日志后保持不变。
"""

import logging
import os

import pytest

import logger as logmod


def test_logger_instance_and_level():
    assert logmod.logger.name == 'bookkeeping', "logger 名称错误"
    assert logmod.logger.level == logging.DEBUG, "日志级别错误"
    assert logmod.logger.handlers, "logger 未配置任何 handler"
    assert any(type(h) is logging.FileHandler for h in logmod.logger.handlers), "缺少文件 handler"


def test_logger_writes_to_file():
    logmod.logger.info('测试日志信息')
    for h in logmod.logger.handlers:
        h.flush()
    with open(logmod.LOG_FILE, encoding='utf-8') as f:
        content = f.read()
    assert '测试日志信息' in content, "日志内容未写入文件"
    assert os.path.getsize(logmod.LOG_FILE) > 0, "日志文件为空"


def test_logger_format_contains_fields():
    logmod.logger.error('格式验证消息')
    for h in logmod.logger.handlers:
        h.flush()
    with open(logmod.LOG_FILE, encoding='utf-8') as f:
        line = next(l for l in f if '格式验证消息' in l)
    assert '[' in line and ']' in line, "缺少日志级别字段"
    assert '[ERROR]' in line, "日志级别错误"
    assert 'test_logger' in line, "缺少模块信息"
    assert '格式验证消息' in line, "缺少消息内容"
    assert line.split(' ')[0].count('-') == 2, "缺少时间戳（YYYY-MM-DD）"


def test_validation_error_behavior_unchanged(data_dir):
    from controller import add_record
    from exceptions import ValidationError
    with pytest.raises(ValidationError) as ei:
        add_record('2026-08-01', '收入', 'abc', 'x')
    assert str(ei.value) == '金额必须是数字！', "ValidationError 提示文字被改变"


def test_storage_error_behavior_unchanged(tmp_path):
    import storage
    from exceptions import StorageError
    rp = str(tmp_path / 'bad.json')
    with open(rp, 'w', encoding='utf-8') as f:
        f.write('{ 坏数据')
    with pytest.raises(StorageError) as ei:
        storage.load_records(rp)
    assert '读取记录文件失败' in str(ei.value), "StorageError 提示文字被改变"