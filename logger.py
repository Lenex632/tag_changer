import logging.config
from pathlib import Path
import sys


file = Path(Path(__file__).parent, 'tag_changer.log')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s]:  %(message)s [%(filename)s::%(name)s::%(funcName)s::%(lineno)d]",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console_handlers": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": file,
            "maxBytes": 1024 * 1024,
            "backupCount": 5
        }
    },
    "loggers": {
        "TagChanger": {"handlers": ["console_handlers", "file_handler"], "level": "INFO"},
        "DBController": {"handlers": ["console_handlers", "file_handler"], "level": "INFO"},
        "Settings": {"handlers": ["console_handlers", "file_handler"], "level": "DEBUG"},
        "App": {"handlers": ["console_handlers", "file_handler"], "level": "DEBUG"},
    }
}


def set_up_logger_config():
    logging.config.dictConfig(LOGGING)
