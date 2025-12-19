import contextvars
import logging
import logging.config
from pathlib import Path
from typing import Optional


request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


def setup_logging(
    *,
    log_file: Optional[str | Path] = None,
    level: str = "INFO",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
) -> None:
    log_path = Path(log_file) if log_file else Path(__file__).resolve().parent.parent / "logs" / "app.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"context": {"()": ContextFilter}},
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s [req:%(request_id)s] - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": level,
                    "formatter": "standard",
                    "filters": ["context"],
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": level,
                    "formatter": "standard",
                    "filters": ["context"],
                    "filename": str(log_path),
                    "maxBytes": max_bytes,
                    "backupCount": backup_count,
                    "encoding": "utf-8",
                    "delay": True,
                },
            },
            "root": {"level": level, "handlers": ["console", "file"]},
        }
    )


def set_request_id(value: str) -> None:
    request_id_var.set(value)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name or "app")

