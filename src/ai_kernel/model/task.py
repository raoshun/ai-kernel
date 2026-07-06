"""
RFC-0009: Task Model

This module implements the Task abstraction defined by RFC-0009.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Task:
    """
    Immutable logical objective.

    A Task represents *what* should be achieved.
    """

    objective: str

    id: UUID = field(default_factory=uuid4)

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )
