"""异常处理层：项目统一异常类型。

业务与存储异常通过统一类型向 UI 层传递，
UI 层据此区分提示类型并展示对应提示文字。
"""


class FinanceError(Exception):
    """项目基础异常，所有业务异常的统一基类。"""


class ValidationError(FinanceError):
    """输入校验异常。message 即需要展示给用户的提示文字。"""


class StorageError(FinanceError):
    """数据存储异常（文件读写、JSON 解析失败等）。"""