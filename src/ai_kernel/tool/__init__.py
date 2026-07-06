"""Tool module for the AI Kernel.

This module implements RFC-0006 Tool Interface.
"""

from ai_kernel.tool.interface import (
    Tool,
    get_tool,
    register_tool,
    list_tools,
    get_tool_by_id,
)

from ai_kernel.tool.model import (
    ToolStatus,
    SideEffectClassification,
    ToolMetadata,
    ToolContract,
    ToolInput,
    ToolOutput,
    ToolInvocation,
    ToolDefinition,
    ToolResult,
)

from ai_kernel.tool.backend import (
    ToolBackend,
    InMemoryToolBackend,
    get_backend,
    create_tool,
)

__all__ = [
    # Interface
    "Tool",
    "get_tool",
    "register_tool",
    "list_tools",
    "get_tool_by_id",
    # Model
    "ToolStatus",
    "SideEffectClassification",
    "ToolMetadata",
    "ToolContract",
    "ToolInput",
    "ToolOutput",
    "ToolInvocation",
    "ToolDefinition",
    "ToolResult",
    # Backend
    "ToolBackend",
    "InMemoryToolBackend",
    "get_backend",
    "create_tool",
]