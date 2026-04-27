"""
Issues-suite fixtures.

Provides issue_data factory for unique autotest_ work item payloads.
"""
from __future__ import annotations

import pytest

from src.helpers.test_data import IssueData


@pytest.fixture
def issue_data() -> IssueData:
    return IssueData()