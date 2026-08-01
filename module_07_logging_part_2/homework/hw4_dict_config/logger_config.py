dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "DEBUG",
            "formatter": "base",
        },
        "file": {
            "()": "hw3_level_file_handler.logger_helper.LevelFileHandler",
            "level": "DEBUG",
            "formatter": "base",
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "utils": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}