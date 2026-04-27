"""
StepLogger — custom logger with STEP / ASSERT / ERROR levels.

Writes timestamped human-readable lines to per-test log files and
attaches them to the Allure report on test completion.
"""
from __future__ import annotations

import logging
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

import allure

from src.helpers.config import settings

# DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
STEP_LEVEL = 25
ASSERT_LEVEL = 26

logging.addLevelName(STEP_LEVEL, "STEP")
logging.addLevelName(ASSERT_LEVEL, "ASSERT")


class StepLogger:
    def __init__(self, test_name: str) -> None:
        self.test_name = test_name
        safe_name = test_name.replace("/", "_").replace("::", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file: Path = settings.logs_dir / f"{safe_name}_{timestamp}.log"

        self._logger = logging.getLogger(f"plane_e2e.{test_name}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False

        self._logger.handlers.clear()

        fmt = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(fmt)
        stream.setLevel(logging.DEBUG)
        self._logger.addHandler(stream)

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setFormatter(fmt)
        file_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(file_handler)

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def step(self, msg: str) -> None:
        self._logger.log(STEP_LEVEL, msg)

    def assertion(self, msg: str, passed: bool = True) -> None:
        status = "PASSED" if passed else "FAILED"
        self._logger.log(ASSERT_LEVEL, f"{msg} -- {status}")

    @contextmanager
    def allure_step(self, title: str) -> Iterator[None]:
        self.step(title)
        with allure.step(title):
            yield

    def attach_log_to_allure(self) -> None:
        if not self.log_file.exists():
            return
        try:
            content = self.log_file.read_text(encoding="utf-8")
            allure.attach(
                body=content,
                name=f"test_log_{self.test_name}",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception as e:
            print(f"[logger] Failed to attach log: {e}", file=sys.stderr)

    def close(self) -> None:
        for h in self._logger.handlers[:]:
            h.close()
            self._logger.removeHandler(h)