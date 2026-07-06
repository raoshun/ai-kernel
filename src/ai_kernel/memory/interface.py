"""
RFC-0008: Memory Interface

Defines the operations exposed to the Kernel.
This is the main entry point for the Memory subsystem.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ai_kernel._logging import memory_logger
from ai_kernel.memory.backend import InMemoryBackend, MemoryBackend
from ai_kernel.memory.model import MemoryObject, MemoryQuery, MemoryScope


class Memory:
    """
    The main Memory interface exposed to the Kernel.
    
    Provides operations:
    - Store: Save new memory objects
    - Query: Retrieve memories by various criteria
    - Update: Modify existing memories
    - Delete: Remove memories
    
    Adheres to RFC-0008 Memory Architecture.
    """
    
    def __init__(self, backend: Optional[MemoryBackend] = None):
        """
        Initialize the Memory interface.
        
        Args:
            backend: The storage backend to use. Defaults to InMemoryBackend.
        """
        self.backend = backend or InMemoryBackend()
        memory_logger.info("Memory Interface initialized")
    
    def store(
        self,
        content: str,
        scope: MemoryScope,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> MemoryObject:
        """
        Store a new memory object.
        
        Args:
            content: The memory content to store
            scope: The scope/boundary for this memory
            metadata: Optional metadata dictionary
            tags: Optional list of tags
            
        Returns:
            The created MemoryObject
        """
        memory = MemoryObject(
            content=content,
            scope=scope,
            metadata=metadata or {},
            tags=tags or []
        )
        self.backend.store(memory)
        return memory
    
    def query(
        self,
        scope: Optional[MemoryScope] = None,
        keywords: Optional[List[str]] = None,
        metadata_filters: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[MemoryObject]:
        """
        Query memory objects by various criteria.
        
        Args:
            scope: Filter by memory scope
            keywords: Filter by keywords in content
            metadata_filters: Filter by metadata key-value pairs
            tags: Filter by tags
            limit: Maximum number of results
            
        Returns:
            List of matching MemoryObject instances
        """
        query = MemoryQuery(
            scope=scope,
            keywords=keywords or [],
            metadata_filters=metadata_filters or {},
            tags=tags or [],
            limit=limit
        )
        return self.backend.retrieve(query)
    
    def update(
        self,
        memory_id: str,
        new_content: Optional[str] = None,
        new_metadata: Optional[Dict[str, Any]] = None,
        add_tags: Optional[List[str]] = None,
        remove_tags: Optional[List[str]] = None
    ) -> Optional[MemoryObject]:
        """
        Update an existing memory object.
        
        Args:
            memory_id: The ID of the memory to update
            new_content: New content (if provided)
            new_metadata: New metadata (if provided, merged with existing)
            add_tags: Tags to add
            remove_tags: Tags to remove
            
        Returns:
            The updated MemoryObject, or None if not found
        """
        memory = self.backend.get_by_id(memory_id)
        if memory is None:
            memory_logger.warning(f"Memory {memory_id} not found for update")
            return None
        
        if new_content:
            memory.update_content(new_content)
        
        if new_metadata:
            memory.metadata.update(new_metadata)
        
        if add_tags:
            for tag in add_tags:
                memory.add_tag(tag)
        
        if remove_tags:
            for tag in remove_tags:
                memory.remove_tag(tag)
        
        self.backend.update(memory)
        return memory
    
    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory object.
        
        Args:
            memory_id: The ID of the memory to delete
            
        Returns:
            True if deleted, False if not found
        """
        return self.backend.delete(memory_id)
    
    def get(self, memory_id: str) -> Optional[MemoryObject]:
        """
        Retrieve a specific memory by ID.
        
        Args:
            memory_id: The unique identifier
            
        Returns:
            The MemoryObject if found, None otherwise
        """
        return self.backend.get_by_id(memory_id)
    
    def list_by_scope(self, scope: MemoryScope) -> List[MemoryObject]:
        """
        List all memories in a specific scope.
        
        Args:
            scope: The scope to filter by
            
        Returns:
            List of MemoryObject instances
        """
        return self.backend.list_by_scope(scope)
    
    def clear_scope(self, scope: MemoryScope) -> int:
        """
        Clear all memories in a specific scope.
        
        Args:
            scope: The scope to clear
            
        Returns:
            Number of memories cleared
        """
        return self.backend.clear_scope(scope)


# Factory function for lazy initialization
_memory_instance = None

def get_memory() -> Memory:
    """Get the singleton Memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = Memory()
    return _memory_instance

# Backward compatibility alias
memory = get_memory()