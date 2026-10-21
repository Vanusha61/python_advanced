from pathlib import Path

# Корень проекта — на 2 уровня выше от текущего файла (если extensions.py в app/)
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
dict_config_crud = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "backupCount": 3,
            "level": "ERROR",
            "formatter": "verbose",
            "filename": f"{LOG_DIR}/error_crud.log",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "crud_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
    "filters": {},
    "root": {},
}

dict_config_api = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "backupCount": 3,
            "level": "ERROR",
            "formatter": "verbose",
            "filename": f"{LOG_DIR}/error_api.log",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "api_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
    "filters": {},
    "root": {},
}
