"""
RFC-0008: Memory Architecture

The Memory subsystem provides a persistent abstraction for storing, retrieving,
and managing cognitive state required by agents during planning and execution.
"""

from ai_kernel.memory.interface import Memory, memory
from ai_kernel.memory.model import MemoryObject, MemoryQuery, MemoryScope
from ai_kernel.memory.backend import MemoryBackend, InMemoryBackend

__all__ = [
    "Memory",
    "memory",
    "MemoryObject",
    "MemoryQuery", 
    "MemoryScope",
    "MemoryBackend",
    "InMemoryBackend",
]