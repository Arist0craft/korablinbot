import logging
from pathlib import Path
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    if not (logs_dir := Path(__file__).resolve().parent.parent / "logs").exists():
        logs_dir.mkdir()
    today = datetime.now().strftime("%Y_%m_%d")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(logs_dir / f"{today}.log")
    fmt = logging.Formatter("%(asctime)s [%(levelname)s](%(name)s) - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    return logger
