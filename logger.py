import os
import logging
import logging.config
from pathlib import Path
import sys


file = Path(Path(__file__).parent, 'logs/tag_changer.log')
error = os.path.join(os.path.dirname(__file__), "logs/error.log")


def filter(record):
    return record.levelno < logging.CRITICAL


# TODO:
#   сделать, чтобы информация о строчках файла выводилась только при ошибках, либо немного разделить, потому что сейчас в INFO слишком много мусора
#   почему-то логирование в файл не работает, надо понять почему
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s]:  %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "extended": {
            "format": "[%(asctime)s] [%(levelname)s]:  %(message)s [%(filename)s::%(name)s::%(funcName)s::%(lineno)d]",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            # "stream": sys.stdout,
            "filters": [filter]
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": file,
            "maxBytes": 1024 * 1024,
            "backupCount": 5,
            "filters": [filter]
        }
    },
    "loggers": {
        "TagChanger": {"handlers": ["console_handler", "file_handler"], "level": "INFO"},
        "DBController": {"handlers": ["console_handler", "file_handler"], "level": "INFO"},
        "Config": {"handlers": ["console_handler", "file_handler"], "level": "DEBUG"},
        "UI": {"handlers": ["console_handler", "file_handler"], "level": "DEBUG"},
    }
}


def set_up_logger_config():
    logging.config.dictConfig(LOGGING)

