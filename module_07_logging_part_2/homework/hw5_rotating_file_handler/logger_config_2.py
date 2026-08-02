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
            "class": "logging.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "filename":"utils.log",
            "mode": "a",
            "when": "H",
            "interval": 10,
            "backupCount": 1,
        }
    },
    "loggers": {
        "utils": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}