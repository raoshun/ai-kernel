from dataclasses import dataclass, field
from typing import List, Dict, Any, Literal
from datetime import datetime

# ===============================================================
# 1. TERMINOLOGY MAPPING (RFC-0000 Compliance)
# ===============================================================

@dataclass(frozen=True)
class Capability:
    """A defined ability possessed by an entity."""
    name: str  # e.g., 'READ_FILE', 'INITIATE_NETWORK_CALL'
    description: str
    scope: str # The scope/resource this capability applies to

@dataclass(frozen=True)
class Permission:
    """The right granted for a specific action."""
    action: str  # e.g., 'read', 'write', 'execute'
    target_capability: Capability # Which capability is being acted upon
    effect: Literal['ALLOW', 'DENY']

@dataclass(frozen=True)
class Authority:
    """The source of the right (e.g., User ID, Service Account)."""
    principal_id: str
    role: str  # e.g., 'ADMIN', 'SERVICE_USER'

# ===============================================================
# 2. EXECUTION & GOAL MODELING (RFC-0001/RFC-0010 Compliance)
# ===============================================================

@dataclass(frozen=True)
class Goal:
    """The ultimate objective derived from user intent."""
    goal_id: str
    description: str
    expected_output_format: str # e.g., JSON Schema, Plain Text
    priority: int = 5

@dataclass(frozen=True)
class Task:
    """A discrete, actionable step towards a Goal."""
    task_id: str
    description: str
    required_capabilities: List[str] # Names of capabilities needed
    dependencies: List[str]       # task_id dependencies
    max_attempts: int = 3

@dataclass(frozen=True)
class ExecutionStep:
    """A single step taken during execution, linking to tooling."""
    tool_name: str
    input_params: Dict[str, Any]
    actual_output: str # The raw output received from the tool

# ===============================================================
# 3. AUDITING AND STATE (RFC-0007 Compliance)
# ===============================================================

@dataclass(frozen=True)
class AuditRecord:
    """Immutable record of any significant event or decision."""
    source_component: str = 'SYSTEM'
    severity: Literal['INFO', 'WARNING', 'CRITICAL'] = 'INFO'
    message: str = ''
    timestamp: datetime = field(default_factory=datetime.now)
    related_ids: List[str] = field(default_factory=list) # Goal IDs, Task IDs etc.

