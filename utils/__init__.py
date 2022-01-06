import logging
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, debug: bool = False, with_function: bool = False) -> logging.Logger:
    if not (logs_dir := Path(__file__).resolve().parent.parent / "logs").exists():
        logs_dir.mkdir()
    today = datetime.now().strftime("%Y_%m_%d")
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO) if not debug else logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(logs_dir / f"{today}.log")
    fmt_fnct = ":%(funcName)s" if with_function else ""
    fmt = logging.Formatter(f"%(asctime)s [%(levelname)s](%(name)s{fmt_fnct}) - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    return logger
