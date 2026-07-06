"""
RFC-0008: Memory Model

Defines memory objects and scopes for the Memory subsystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


class MemoryScope(str, Enum):
    """Defines the scope/boundary of a memory object."""

    GLOBAL = "global"
    WORKSPACE = "workspace"
    SESSION = "session"
    AGENT = "agent"
    USER = "user"


@dataclass
class MemoryObject:
    """
    A unit of persistent information in the Memory subsystem.
    
    Each Memory Object contains:
    - identifier: unique ID
    - content: the actual memory content
    - metadata: additional context
    - scope: the boundary this memory belongs to
    - timestamps: creation and update times
    """

    content: str
    scope: MemoryScope
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Update timestamps on initialization."""
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def update_content(self, new_content: str) -> None:
        """Update the memory content and timestamp."""
        self.content = new_content
        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: str) -> None:
        """Add a tag to this memory object."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from this memory object."""
        if tag in self.tags:
            self.tags.remove(tag)


@dataclass
class MemoryQuery:
    """
    A query specification for retrieving memory objects.
    """

    scope: Optional[MemoryScope] = None
    keywords: list[str] = field(default_factory=list)
    metadata_filters: Dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    limit: int = 10
    since: Optional[datetime] = None