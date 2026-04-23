"""Root conftest. Полные фикстуры будут добавлены в этапе 4."""
from __future__ import annotations

import sys
from pathlib import Path

# Делаем src/ импортируемым как пакет из любого теста
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))