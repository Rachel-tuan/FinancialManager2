"""数据模型层：账单记录与月度目标的领域模型。

与现有 JSON 存储格式一一对应（读写后格式不变）：
- records.json: [{date, category, amount, note}, ...]
- goals.json:   {月份: 金额, ...}
"""

from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    """账单分类，JSON 中存储其 value 字符串。"""

    INCOME = '收入'
    EXPENSE = '支出'

    @classmethod
    def from_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f'无效的账单分类: {value!r}（应为 收入/支出）') from None


@dataclass
class Record:
    """单条账单记录，对应 records.json 中的一个元素。"""

    date: str
    category: Category
    amount: float
    note: str = ''

    def to_dict(self):
        """转换为 JSON 存储字典，键顺序与现有文件一致。"""
        return {
            'date': self.date,
            'category': self.category.value,
            'amount': self.amount,
            'note': self.note,
        }

    @classmethod
    def from_dict(cls, data):
        """从 JSON 存储字典构造 Record。"""
        return cls(
            date=data['date'],
            category=Category.from_value(data['category']),
            amount=float(data['amount']),
            note=data.get('note', ''),
        )


@dataclass
class Goal:
    """单个月度支出目标，对应 goals.json 中的一个键值对。"""

    month: str
    amount: float


class Goals:
    """月度目标集合，对应 goals.json 的 {月份: 金额} 字典。"""

    def __init__(self, items=None):
        self._items = dict(items or {})

    def get(self, month):
        """返回指定月份目标金额；未设置时返回 None。"""
        return self._items.get(month)

    def set(self, month, amount):
        """设置指定月份的目标金额。"""
        self._items[month] = amount

    def to_dict(self):
        """转换为 JSON 存储字典。"""
        return dict(self._items)

    @classmethod
    def from_dict(cls, data):
        """从 JSON 存储字典构造 Goals。"""
        return cls(data or {})