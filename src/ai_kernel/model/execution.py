"""
RFC-0010: Execution Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

from ai_kernel.model.task import Task


class ExecutionState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class Execution:
    """
    Runtime instance of a Task.
    """

    task: Task
    id: UUID = field(default_factory=uuid4)
    state: ExecutionState = ExecutionState.PENDING
    result: str | None = None
    error: str | None = None
