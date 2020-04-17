import distutils
import os
from datetime import datetime
from enum import Enum
from textwrap import dedent


class LogLevel(Enum):
    ERROR = "error"
    INFO = "info"
    DEBUG = "debug"


def log(message: str, log_level: LogLevel = LogLevel.INFO):
    time = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
    timed_message = f"{time} - {log_level} - {dedent(message)}"
    print(timed_message)


class MissingParameterException(Exception):
    pass


def get_required_env(name):
    param = os.getenv(name, None)
    if param is None:
        raise MissingParameterException(f"<8922e16> {name} is required parameter")
    return param

def to_bool(value) -> bool:
    if value is bool:
        return value
    if value is str:
        return distutils.util.strtobool(value)
    raise ValueError("<c8f3984b> Value must by string or bool")
