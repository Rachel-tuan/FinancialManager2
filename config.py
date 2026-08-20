"""配置与常量管理层：集中管理项目中的配置与常量。

JSON 文件路径、账单分类、日期格式等集中定义于此，避免各层硬编码。
"""

# 文件配置
DATA_FILE = 'records.json'
GOAL_FILE = 'goals.json'

# 分类常量
INCOME = '收入'
EXPENSE = '支出'

# 日期相关常量
MONTH_FORMAT = '%Y-%m'
DATE_FORMAT = '%Y-%m-%d'