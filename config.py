"""配置管理层：集中管理项目配置。

AppConfig 提供实例化配置对象，旧模块级常量保留为兼容别名。
"""

import os


class AppConfig:
    """项目配置对象。"""

    def __init__(self):
        self.data_file = 'records.json'
        self.goal_file = 'goals.json'
        self.date_format = '%Y-%m-%d'
        self.month_format = '%Y-%m'
        self.log_file = os.environ.get('LOG_FILE', 'bookkeeping.log')


config = AppConfig()

# ---- 兼容别名（旧常量，保持既有引用可用） ----
DATA_FILE = config.data_file
GOAL_FILE = config.goal_file
INCOME = '收入'
EXPENSE = '支出'
MONTH_FORMAT = config.month_format
DATE_FORMAT = config.date_format