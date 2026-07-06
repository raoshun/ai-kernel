"""Tool backend and registry for the AI Kernel."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ai_kernel.tool.model import (
    SideEffectClassification,
    ToolContract,
    ToolDefinition,
    ToolInvocation,
    ToolMetadata,
    ToolStatus,
)


class ToolBackend(ABC):
    """Abstract backend for Tool storage and execution."""

    @abstractmethod
    def register(self, tool: ToolDefinition) -> None:
        """Register a Tool."""
        raise NotImplementedError

    @abstractmethod
    def unregister(self, tool_id: str) -> None:
        """Unregister a Tool."""
        raise NotImplementedError

    @abstractmethod
    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        """Get a Tool by ID."""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[ToolDefinition]:
        """List all registered Tools."""
        raise NotImplementedError

    @abstractmethod
    def list_by_capability(self, capability: str) -> List[ToolDefinition]:
        """List Tools requiring a specific capability."""
        raise NotImplementedError

    @abstractmethod
    def create_invocation(
        self,
        tool_id: str,
        tool_identifier: str,
        message_id: Optional[str] = None,
        task_id: Optional[str] = None,
        execution_context_id: Optional[str] = None,
        decision_id: Optional[str] = None,
    ) -> ToolInvocation:
        """Create a new Tool invocation."""
        raise NotImplementedError

    @abstractmethod
    def get_invocation(self, invocation_id: str) -> Optional[ToolInvocation]:
        """Get a Tool invocation by ID."""
        raise NotImplementedError

    @abstractmethod
    def update_invocation_status(
        self, invocation_id: str, status: ToolStatus
    ) -> None:
        """Update invocation status."""
        raise NotImplementedError


class InMemoryToolBackend(ToolBackend):
    """In-memory implementation of Tool backend."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}
        self._invocations: Dict[str, ToolInvocation] = {}
        self._invocation_counter: int = 0

    def register(self, tool: ToolDefinition) -> None:
        tool_id = tool.identifier
        self._tools[tool_id] = tool

    def unregister(self, tool_id: str) -> None:
        self._tools.pop(tool_id, None)

    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        return self._tools.get(tool_id)

    def list_all(self) -> List[ToolDefinition]:
        return list(self._tools.values())

    def list_by_capability(self, capability: str) -> List[ToolDefinition]:
        return [
            tool
            for tool in self._tools.values()
            if capability in tool.required_capabilities
        ]

    def create_invocation(
        self,
        tool_id: str,
        tool_identifier: str,
        message_id: Optional[str] = None,
        task_id: Optional[str] = None,
        execution_context_id: Optional[str] = None,
        decision_id: Optional[str] = None,
    ) -> ToolInvocation:
        from ai_kernel.tool.model import ToolInput

        self._invocation_counter += 1
        invocation_id = f"invocation-{self._invocation_counter}"

        invocation = ToolInvocation(
            id=invocation_id,
            tool_id=tool_id,
            tool_identifier=tool_identifier,
            input=ToolInput(
                message_id=message_id,
                task_id=task_id,
                execution_context_id=execution_context_id,
                decision_id=decision_id,
            ),
        )
        self._invocations[invocation_id] = invocation
        return invocation

    def get_invocation(self, invocation_id: str) -> Optional[ToolInvocation]:
        return self._invocations.get(invocation_id)

    def update_invocation_status(
        self, invocation_id: str, status: ToolStatus
    ) -> None:
        invocation = self._invocations.get(invocation_id)
        if invocation:
            invocation.status = status


# Global backend instance
_backend: Optional[InMemoryToolBackend] = None


def get_backend() -> InMemoryToolBackend:
    """Get the global Tool backend instance."""
    global _backend
    if _backend is None:
        _backend = InMemoryToolBackend()
    return _backend


def create_tool(
    identifier: str,
    description: str,
    version: str,
    required_capabilities: List[str],
    expected_inputs: Dict[str, Any],
    expected_outputs: Dict[str, Any],
    failure_modes: List[str],
    side_effects: List[SideEffectClassification],
    executable: Any = None,
) -> ToolDefinition:
    """Helper to create a ToolDefinition."""
    return ToolDefinition(
        metadata=ToolMetadata(
            identifier=identifier,
            description=description,
            version=version,
            required_capabilities=required_capabilities,
            expected_inputs=expected_inputs,
            expected_outputs=expected_outputs,
            failure_modes=failure_modes,
            side_effects=side_effects,
        ),
        contract=ToolContract(),
        executable=executable,
    )