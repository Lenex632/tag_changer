import logging.config
import sys

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(name)s] [%(levelname)s]:  %(message)s (%(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console_handlers": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": sys.stdout
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": 'Log.log',
            "maxBytes": 1024 * 1024,
            "backupCount": 5
        }
    },
    "loggers": {
        "": {"handlers": ["console_handlers", "file_handler"], "level": "DEBUG"}
    }
}


def set_up_logger_config():
    logging.config.dictConfig(LOGGING)
