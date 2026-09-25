"""pytest 共享配置：路径注入与数据隔离。"""

import os
import sys
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_DIR)
STUBS_DIR = os.path.join(TESTS_DIR, 'stubs')

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, STUBS_DIR)

# 将日志文件重定向到临时目录，避免测试在项目根目录生成 bookkeeping.log
os.environ.setdefault('LOG_FILE', os.path.join(tempfile.mkdtemp(prefix='bookkeeping_log_'), 'test.log'))

import pytest


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    """切换到独立临时工作目录，隔离默认数据文件（records.json / goals.json）。"""
    monkeypatch.chdir(tmp_path)
    return tmp_path