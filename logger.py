import logging
import logging.config
from pathlib import Path


file = Path(Path(__file__).parent, 'logs/tag_changer.log')
error = Path(Path(__file__).parent, 'logs/error.log')


# INFO: дополнительная обёртка нужна как костыль для Python < 3.11
def make_filter():
    def filter(record):
        return record.levelno < logging.CRITICAL
    return filter


LOGGING = {
    'version': 1,
    'filters': {
        'filter': {'()': make_filter}
    },
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)-9s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'extended': {
            'format': '[%(asctime)s] %(levelname)-9s: %(message)s\n[%(filename)s:%(lineno)d %(name)s.%(funcName)s]',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filters': ['filter']
        },
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': file,
            'maxBytes': 1024 * 1024,
            'backupCount': 5,
            'filters': ['filter']
        },
        'error_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'CRITICAL',
            'formatter': 'extended',
            'filename': error,
            'maxBytes': 1024 * 1024,
            'backupCount': 5
        }
    },
    'loggers': {
        'TagChanger': {'handlers': ['console_handler', 'file_handler', 'error_handler'], 'level': 'DEBUG'},
        'DBController': {'handlers': ['console_handler', 'file_handler', 'error_handler'], 'level': 'DEBUG'},
        'Config': {'handlers': ['console_handler', 'file_handler', 'error_handler'], 'level': 'DEBUG'},
        'Main': {'handlers': ['console_handler', 'file_handler', 'error_handler'], 'level': 'DEBUG'},
    }
}


def set_up_logger_config():
    logging.config.dictConfig(LOGGING)


if __name__ == "__main__":
    set_up_logger_config()
    from logging import getLogger

    logger = getLogger('TagChanger')
    logger.info(file)
    logger.info(error)
    logger.info('test_log')
    logger.error('test_error')
    logger.critical('test_critical')

