"""
RFC-0008: Memory Backend

Provides the storage abstraction layer for the Memory subsystem.
This module defines the backend interface that different storage implementations must follow.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ai_kernel._logging import memory_logger
from ai_kernel.memory.model import MemoryObject, MemoryQuery, MemoryScope


class MemoryBackend(ABC):
    """
    Abstract base class for memory storage backends.
    
    All memory backends MUST implement this interface to ensure
    consistent behavior regardless of the underlying storage technology.
    """

    @abstractmethod
    def store(self, memory: MemoryObject) -> None:
        """
        Store a memory object.
        
        Args:
            memory: The MemoryObject to store
        """
        pass

    @abstractmethod
    def retrieve(self, query: MemoryQuery) -> List[MemoryObject]:
        """
        Retrieve memory objects matching the query.
        
        Args:
            query: The MemoryQuery specifying search criteria
            
        Returns:
            List of matching MemoryObject instances
        """
        pass

    @abstractmethod
    def update(self, memory: MemoryObject) -> None:
        """
        Update an existing memory object.
        
        Args:
            memory: The MemoryObject with updated content
        """
        pass

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory object by its ID.
        
        Args:
            memory_id: The unique identifier of the memory
            
        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def get_by_id(self, memory_id: str) -> Optional[MemoryObject]:
        """
        Retrieve a specific memory object by ID.
        
        Args:
            memory_id: The unique identifier of the memory
            
        Returns:
            The MemoryObject if found, None otherwise
        """
        pass

    @abstractmethod
    def list_by_scope(self, scope: MemoryScope) -> List[MemoryObject]:
        """
        List all memory objects within a specific scope.
        
        Args:
            scope: The MemoryScope to filter by
            
        Returns:
            List of MemoryObject instances in the scope
        """
        pass

    @abstractmethod
    def clear_scope(self, scope: MemoryScope) -> int:
        """
        Clear all memories within a specific scope.
        
        Args:
            scope: The MemoryScope to clear
            
        Returns:
            Number of memories cleared
        """
        pass


class InMemoryBackend(MemoryBackend):
    """
    Simple in-memory implementation for MVP.
    
    This backend stores all memories in memory and is suitable for
    single-process applications. Data is lost on application restart.
    """

    def __init__(self):
        self._memories: Dict[str, MemoryObject] = {}
        memory_logger.info("InMemoryBackend initialized: Using in-memory storage.")

    def store(self, memory: MemoryObject) -> None:
        """Store a memory object in memory."""
        self._memories[str(memory.id)] = memory
        memory_logger.info(f"Stored: {memory.id} ({memory.scope})")

    def retrieve(self, query: MemoryQuery) -> List[MemoryObject]:
        """Retrieve memories matching the query."""
        results = []
        
        for memory in self._memories.values():
            if self._matches_query(memory, query):
                results.append(memory)
        
        # Apply limit
        return results[:query.limit]
    
    def _matches_query(self, memory: MemoryObject, query: MemoryQuery) -> bool:
        """Check if a memory object matches the query criteria."""
        # Filter by scope
        if query.scope and memory.scope != query.scope:
            return False
        
        # Filter by keywords
        if query.keywords:
            if not any(kw.lower() in memory.content.lower() for kw in query.keywords):
                return False
        
        # Filter by tags
        if query.tags:
            if not any(tag in memory.tags for tag in query.tags):
                return False
        
        # Filter by metadata
        if query.metadata_filters:
            for key, value in query.metadata_filters.items():
                if memory.metadata.get(key) != value:
                    return False
        
        # Filter by timestamp
        if query.since and memory.created_at < query.since:
            return False
        
        return True

    def update(self, memory: MemoryObject) -> None:
        """Update an existing memory object."""
        if str(memory.id) in self._memories:
            self._memories[str(memory.id)] = memory
            memory_logger.info(f"Updated: {memory.id}")
        else:
            memory_logger.warning(f"Memory {memory.id} not found for update")

    def delete(self, memory_id: str) -> bool:
        """Delete a memory object by ID."""
        if memory_id in self._memories:
            del self._memories[memory_id]
            memory_logger.info(f"Deleted: {memory_id}")
            return True
        return False

    def get_by_id(self, memory_id: str) -> Optional[MemoryObject]:
        """Get a specific memory by ID."""
        return self._memories.get(memory_id)

    def list_by_scope(self, scope: MemoryScope) -> List[MemoryObject]:
        """List all memories in a scope."""
        return [m for m in self._memories.values() if m.scope == scope]

    def clear_scope(self, scope: MemoryScope) -> int:
        """Clear all memories in a scope."""
        to_delete = [mid for mid, m in self._memories.items() if m.scope == scope]
        for mid in to_delete:
            del self._memories[mid]
        memory_logger.info(f"Cleared {len(to_delete)} memories from scope: {scope}")
        return len(to_delete)