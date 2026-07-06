from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class BasePlugin:
    """Minimal plugin interface used by the Kernel."""

    identifier: str
    name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def initialize(self) -> None:
        """Perform plugin initialization."""
