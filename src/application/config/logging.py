import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True
        },
        "coilcast": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
