import logging
from enum import StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s-%(message)s-%(pathname)s-%(asctime)s"
class LogLevels(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def config_level(log_level: str = LogLevels.ERROR):
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.ERROR)
        return

    if log_level == LogLevels.DEBUG:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT_DEBUG)
        return
    
    logging.basicConfig(level=log_level)

