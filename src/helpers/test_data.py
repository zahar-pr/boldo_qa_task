"""
Faker-based factories for test data with autotest_ prefix.

Each factory generates a unique entity (project, issue, page, cycle)
prefixed with autotest_ + uuid suffix to keep runs isolated.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from faker import Faker

fake = Faker()
TEST_PREFIX = "autotest"


def _uid() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class ProjectData:
    name: str = field(default_factory=lambda: f"{TEST_PREFIX}_project_{_uid()}")
    identifier: str = field(default_factory=lambda: f"AT{_uid()[:3].upper()}")
    description: str = field(default_factory=lambda: fake.sentence(nb_words=8))


@dataclass
class IssueData:
    title: str = field(default_factory=lambda: f"{TEST_PREFIX}_issue_{_uid()}")
    description: str = field(default_factory=lambda: fake.paragraph(nb_sentences=2))


@dataclass
class WorkspaceData:
    name: str = field(default_factory=lambda: f"{TEST_PREFIX}_ws_{_uid()}")


@dataclass
class CycleData:
    name: str = field(default_factory=lambda: f"{TEST_PREFIX}_cycle_{_uid()}")
    description: str = field(default_factory=lambda: fake.sentence(nb_words=6))


@dataclass
class PageData:
    title: str = field(default_factory=lambda: f"{TEST_PREFIX}_page_{_uid()}")
    content: str = field(default_factory=lambda: fake.text(max_nb_chars=200))


@dataclass
class CommentData:
    text: str = field(default_factory=lambda: fake.sentence(nb_words=10))