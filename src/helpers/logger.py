"""Кастомный логгер для E2E тестов.

Требования ТЗ:
- Уровни: INFO, STEP, ASSERT, ERROR, WARNING
- Таймстампы в каждой строке
- Запись в файл + прикрепление к Allure
- Интеграция с allure.step для автоматического шага в отчёте

Почему свой логгер поверх logging:
- Нужны кастомные уровни (STEP, ASSERT) которых нет в stdlib.
- Нужна автоматическая обёртка в allure.step без повторения в тестах.
- Нужен per-test файл с логами (не один на весь прогон).
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

# Кастомные уровни логирования.
# Значения выбраны так, чтобы не конфликтовать с stdlib:
# DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
STEP_LEVEL = 25  # между INFO и WARNING — видно всегда
ASSERT_LEVEL = 26

logging.addLevelName(STEP_LEVEL, "STEP")
logging.addLevelName(ASSERT_LEVEL, "ASSERT")


class StepLogger:
    """Логгер одного теста.

    Создаётся в фикстуре, уничтожается после теста.
    Пишет в консоль + в файл logs/<test_name>_<timestamp>.log
    + дублирует в Allure как attachment в конце теста.
    """

    def __init__(self, test_name: str) -> None:
        self.test_name = test_name
        safe_name = test_name.replace("/", "_").replace("::", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file: Path = settings.logs_dir / f"{safe_name}_{timestamp}.log"

        self._logger = logging.getLogger(f"plane_e2e.{test_name}")
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False

        # Чистим обработчики на случай повторного создания
        # (pytest иногда переиспользует логгеры между тестами)
        self._logger.handlers.clear()

        fmt = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Консоль
        stream = logging.StreamHandler(sys.stdout)
        stream.setFormatter(fmt)
        stream.setLevel(logging.DEBUG)
        self._logger.addHandler(stream)

        # Файл
        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setFormatter(fmt)
        file_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(file_handler)

    # --- Уровни ---
    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)

    def step(self, msg: str) -> None:
        """STEP — действие теста (кликнул, ввёл, перешёл)."""
        self._logger.log(STEP_LEVEL, msg)

    def assertion(self, msg: str, passed: bool = True) -> None:
        """ASSERT — проверка. Пишет PASSED/FAILED в конце строки."""
        status = "PASSED" if passed else "FAILED"
        self._logger.log(ASSERT_LEVEL, f"{msg} -- {status}")

    # --- Контекстный менеджер для шага с Allure ---
    @contextmanager
    def allure_step(self, title: str) -> Iterator[None]:
        """Объединяет лог STEP + allure.step.

        Использование:
            with log.allure_step("Fill login form"):
                page.fill(...)
        """
        self.step(title)
        with allure.step(title):
            yield

    # --- Финализация теста ---
    def attach_log_to_allure(self) -> None:
        """Прикрепить весь лог-файл как attachment к Allure отчёту."""
        if not self.log_file.exists():
            return
        try:
            content = self.log_file.read_text(encoding="utf-8")
            allure.attach(
                body=content,
                name=f"test_log_{self.test_name}",
                attachment_type=allure.attachment_type.TEXT,
            )
        except Exception as e:  # noqa: BLE001 — не хотим падать из-за логгера
            # Если упало прикрепление — не роняем тест, просто пишем в stderr.
            print(f"[logger] Failed to attach log: {e}", file=sys.stderr)

    def close(self) -> None:
        """Закрыть все хендлеры (важно на Windows/WSL — иначе лок файла)."""
        for h in self._logger.handlers[:]:
            h.close()
            self._logger.removeHandler(h)