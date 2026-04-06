import logging
import os
from pathlib import Path


def get_logger(name: str = "edgevisionnet") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    report_dir = Path(__file__).resolve().parent / ".." / "results" / "reports"
    report_dir = report_dir.resolve()
    report_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(report_dir / "edgevisionnet.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
