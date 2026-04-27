"""
Project-suite fixtures.

Provides project_data factory that generates unique autotest_ entities
for each test to keep them isolated.
"""
from __future__ import annotations

from typing import Generator

import pytest

from src.helpers.test_data import ProjectData


@pytest.fixture
def project_data() -> ProjectData:
    return ProjectData()