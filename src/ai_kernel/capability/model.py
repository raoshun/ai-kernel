"""
RFC-0002: Capability Model

A Capability is a temporary authorization for an Agent to invoke a defined class of Functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4


class CapabilityType(str, Enum):
    """Standard capability types."""

    SHELL_EXECUTE = "shell.execute"
    FILESYSTEM_READ = "filesystem.read"
    FILESYSTEM_WRITE = "filesystem.write"
    PYTHON_EXECUTE = "python.execute"
    GIT_READ = "git.read"


@dataclass
class Capability:
    """
    A temporary authorization for an agent to invoke functions.

    Capabilities are:
    - explicit: clearly defined
    - task-scoped: bound to a specific task
    - temporary: expire automatically
    - revocable: can be withdrawn at any time
    """

    type: CapabilityType
    task_id: UUID
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set default expiration if not provided."""
        if self.expires_at is None:
            self.expires_at = self.created_at + timedelta(hours=1)

    def is_expired(self) -> bool:
        """Check if capability has expired."""
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        """Check if capability is still valid."""
        return not self.is_expired()
