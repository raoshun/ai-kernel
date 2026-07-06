"""Tool interface for the AI Kernel.

This module provides the main entry point for Tool management and execution,
following RFC-0006 Tool Interface specification.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from ai_kernel.tool.backend import (
    ToolBackend,
    create_tool,
    get_backend,
)
from ai_kernel.tool.model import (
    SideEffectClassification,
    ToolContract,
    ToolDefinition,
    ToolInput,
    ToolInvocation,
    ToolMetadata,
    ToolOutput,
    ToolResult,
    ToolStatus,
)


class Tool:
    """Main interface for Tool management and execution."""

    def __init__(self, backend: Optional[ToolBackend] = None) -> None:
        self._backend = backend or get_backend()

    def register_tool(self, tool: ToolDefinition) -> None:
        """Register a Tool with the Kernel."""
        self._backend.register(tool)

    def unregister_tool(self, tool_id: str) -> None:
        """Unregister a Tool from the Kernel."""
        self._backend.unregister(tool_id)

    def get_tool(self, tool_id: str) -> Optional[ToolDefinition]:
        """Get a Tool by identifier."""
        return self._backend.get(tool_id)

    def list_tools(self) -> List[ToolDefinition]:
        """List all registered Tools."""
        return self._backend.list_all()

    def list_tools_by_capability(self, capability: str) -> List[ToolDefinition]:
        """List Tools requiring a specific capability."""
        return self._backend.list_by_capability(capability)

    def create_invocation(
        self,
        tool_id: str,
        tool_identifier: str,
        message_id: Optional[str] = None,
        task_id: Optional[str] = None,
        execution_context_id: Optional[str] = None,
        decision_id: Optional[str] = None,
    ) -> ToolInvocation:
        """Create a new Tool invocation (Requested state)."""
        return self._backend.create_invocation(
            tool_id=tool_id,
            tool_identifier=tool_identifier,
            message_id=message_id,
            task_id=task_id,
            execution_context_id=execution_context_id,
            decision_id=decision_id,
        )

    def get_invocation(self, invocation_id: str) -> Optional[ToolInvocation]:
        """Get a Tool invocation by ID."""
        return self._backend.get_invocation(invocation_id)

    def authorize_invocation(self, invocation_id: str) -> None:
        """Transition invocation to Authorized state."""
        self._backend.update_invocation_status(invocation_id, ToolStatus.AUTHORIZED)

    def prepare_invocation(self, invocation_id: str) -> None:
        """Transition invocation to Prepared state."""
        self._backend.update_invocation_status(invocation_id, ToolStatus.PREPARED)

    def execute_invocation(
        self,
        invocation_id: str,
        parameters: Dict[str, Any],
    ) -> ToolOutput:
        """Execute a Tool invocation."""
        from ai_kernel.tool.model import ToolOutput

        invocation = self._backend.get_invocation(invocation_id)
        if not invocation:
            raise ValueError(f"Invocation {invocation_id} not found")

        tool = self._backend.get(invocation.tool_id)
        if not tool:
            raise ValueError(f"Tool {invocation.tool_id} not found")

        # Update to Executing state
        self._backend.update_invocation_status(invocation_id, ToolStatus.EXECUTING)
        invocation.started_at = datetime.utcnow()

        # Execute the tool if executable is provided
        result = None
        error = None
        success = True

        try:
            if tool.executable is not None:
                result = tool.executable(**parameters)
            else:
                result = f"Tool {tool.identifier} executed (no executable)"
        except Exception as e:
            success = False
            error = str(e)

        # Set output status
        output_status = ToolStatus.COMPLETED if success else ToolStatus.FAILED
        self._backend.update_invocation_status(invocation_id, output_status)

        output = ToolOutput(
            result=result,
            status=output_status,
            error=error,
        )

        invocation.output = output
        invocation.completed_at = datetime.utcnow()

        return output

    def cancel_invocation(self, invocation_id: str) -> None:
        """Cancel a Tool invocation."""
        self._backend.update_invocation_status(invocation_id, ToolStatus.CANCELLED)


# Global singleton instance
_tool: Optional[Tool] = None


def get_tool() -> Tool:
    """Get the global Tool instance."""
    global _tool
    if _tool is None:
        _tool = Tool()
    return _tool


# Convenience functions matching memory module pattern
def register_tool(
    identifier: str,
    description: str,
    version: str = "1.0.0",
    required_capabilities: Optional[List[str]] = None,
    expected_inputs: Optional[Dict[str, Any]] = None,
    expected_outputs: Optional[Dict[str, Any]] = None,
    failure_modes: Optional[List[str]] = None,
    side_effects: Optional[List[SideEffectClassification]] = None,
    executable: Any = None,
) -> None:
    """Register a new Tool with the Kernel."""
    tool = create_tool(
        identifier=identifier,
        description=description,
        version=version,
        required_capabilities=required_capabilities or [],
        expected_inputs=expected_inputs or {},
        expected_outputs=expected_outputs or [],
        failure_modes=failure_modes or [],
        side_effects=side_effects or [],
        executable=executable,
    )
    get_tool().register_tool(tool)


def list_tools() -> List[ToolDefinition]:
    """List all registered Tools."""
    return get_tool().list_tools()


def get_tool_by_id(tool_id: str) -> Optional[ToolDefinition]:
    """Get a Tool by identifier."""
    return get_tool().get_tool(tool_id)