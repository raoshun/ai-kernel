"""Tool data models for the AI Kernel."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ToolStatus(Enum):
    """Tool invocation status following RFC-0006 lifecycle."""

    REQUESTED = "requested"
    AUTHORIZED = "authorized"
    PREPARED = "prepared"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SideEffectClassification(Enum):
    """Classification of tool side effects."""

    READ_ONLY = "read-only"
    CREATES_RESOURCES = "creates-resources"
    MODIFIES_RESOURCES = "modifies-resources"
    DELETES_RESOURCES = "deletes-resources"
    EXTERNAL_COMMUNICATION = "external-communication"
    IRREVERSIBLE_OPERATIONS = "irreversible-operations"


@dataclass
class ToolMetadata:
    """Metadata describing a Tool's behavior (RFC-0006)."""

    identifier: str
    description: str
    version: str
    required_capabilities: List[str] = field(default_factory=list)
    expected_inputs: Dict[str, Any] = field(default_factory=dict)
    expected_outputs: Dict[str, Any] = field(default_factory=dict)
    failure_modes: List[str] = field(default_factory=list)
    side_effects: List[SideEffectClassification] = field(default_factory=list)
    timeout_seconds: Optional[int] = None


@dataclass
class ToolContract:
    """Contract defining Tool behavior."""

    accepted_inputs: Dict[str, Any] = field(default_factory=dict)
    observable_outputs: Dict[str, Any] = field(default_factory=dict)
    execution_guarantees: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    failure_conditions: List[str] = field(default_factory=list)


@dataclass
class ToolInput:
    """Input for Tool execution."""

    parameters: Dict[str, Any] = field(default_factory=dict)
    message_id: Optional[str] = None
    task_id: Optional[str] = None
    execution_context_id: Optional[str] = None
    decision_id: Optional[str] = None


@dataclass
class ToolOutput:
    """Output from Tool execution."""

    result: Any
    status: ToolStatus
    error: Optional[str] = None
    side_effects_observed: List[str] = field(default_factory=list)
    execution_time_ms: Optional[int] = None


@dataclass
class ToolInvocation:
    """A single Tool invocation record."""

    id: str
    tool_id: str
    tool_identifier: str
    input: ToolInput
    output: Optional[ToolOutput] = None
    status: ToolStatus = ToolStatus.REQUESTED
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class ToolDefinition:
    """Complete Tool definition including metadata and contract."""

    metadata: ToolMetadata
    contract: ToolContract
    executable: Any = field(default=None, repr=False)

    @property
    def identifier(self) -> str:
        return self.metadata.identifier

    @property
    def version(self) -> str:
        return self.metadata.version

    @property
    def required_capabilities(self) -> List[str]:
        return self.metadata.required_capabilities


@dataclass
class ToolResult:
    """Result of a Tool execution, including audit information."""

    success: bool
    tool_id: str
    tool_identifier: str
    output: Optional[ToolOutput] = None
    error_message: Optional[str] = None
    audit_event_id: Optional[str] = None