"""
RFC-0005: Message Protocol

This module implements the message protocol for inter-component communication.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import Any, Mapping


class MessageType(str, Enum):
    """Message types in the protocol."""

    TASK_REQUEST = "task_request"
    EXECUTION_RESPONSE = "execution_response"
    AUDIT_LOG = "audit_log"


@dataclass
class TaskRequest:
    """Request to execute a task."""

    task_id: UUID
    objective: str
    type: MessageType = field(default=MessageType.TASK_REQUEST)
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionResponse:
    """Response from task execution."""

    execution_id: UUID
    task_id: UUID
    state: str
    type: MessageType = field(default=MessageType.EXECUTION_RESPONSE)
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    result: str | None = None
    error: str | None = None


@dataclass
class AuditLog:
    """Audit log entry."""

    execution_id: UUID
    action: str
    description: str
    authorized: bool
    type: MessageType = field(default=MessageType.AUDIT_LOG)
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
