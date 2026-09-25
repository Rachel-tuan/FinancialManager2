"""日志系统：统一日志实例。

使用标准库 logging，输出到控制台与日志文件。
日志文件路径可通过环境变量 LOG_FILE 指定，默认当前目录 bookkeeping.log。
"""

import logging

from config import config

_FORMAT = '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s'


def _create_logger():
    logger = logging.getLogger('bookkeeping')
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        formatter = logging.Formatter(_FORMAT)

        file_handler = logging.FileHandler(config.log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


logger = _create_logger()
LOG_FILE = config.log_file  # 兼容别名


def debug(message, *args, **kwargs):
    logger.debug(message, *args, **kwargs)


def info(message, *args, **kwargs):
    logger.info(message, *args, **kwargs)


def warning(message, *args, **kwargs):
    logger.warning(message, *args, **kwargs)


def error(message, *args, **kwargs):
    logger.error(message, *args, **kwargs)