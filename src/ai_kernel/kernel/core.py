"""
RFC-0004/0013: Kernel Model

The Kernel is the root of trust.

The Kernel is responsible for:
- policy enforcement
- capability management
- execution authorization
- audit logging
- task orchestration
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Protocol
from uuid import UUID

from ai_kernel.capability.model import Capability, CapabilityType
from ai_kernel.message.protocol import AuditLog, ExecutionResponse
from ai_kernel.model.execution import Execution, ExecutionState
from ai_kernel.model.task import Task
from ai_kernel.policy.rules import DefaultPolicies, PolicyDecision, PolicyRule


class AuditLogger:
    """
    Records all meaningful actions.
    Part of separation of authority: auditing is independent.
    """

    def __init__(self):
        self.logs: list[AuditLog] = []
        self.logger = logging.getLogger("kernel.audit")

    def log_execution_start(
        self, execution: Execution, decision: PolicyDecision, reason: str | None = None
    ) -> None:
        """Log execution authorization."""
        entry = AuditLog(
            execution_id=execution.id,
            action="execution_start",
            description=f"Task '{execution.task.objective}' authorization: {decision}",
            authorized=(decision == PolicyDecision.APPROVED),
            reason=reason,
            metadata={"decision": decision.value},
        )
        self.logs.append(entry)
        self.logger.info(f"Execution {entry.action}: {entry.description}")

    def log_execution_result(
        self, execution: Execution, state: ExecutionState, message: str | None = None
    ) -> None:
        """Log execution result."""
        entry = AuditLog(
            execution_id=execution.id,
            action=f"execution_{state.value}",
            description=f"Task execution completed with state: {state}",
            authorized=True,
            metadata={"result_state": state.value},
        )
        self.logs.append(entry)
        self.logger.info(f"Execution {entry.action}: {entry.description}")

    def get_logs(self, execution_id: UUID | None = None) -> list[AuditLog]:
        """Retrieve audit logs."""
        if execution_id:
            return [log for log in self.logs if log.execution_id == execution_id]
        return self.logs.copy()


class CapabilityManager:
    """
    Manages task-scoped capabilities.
    Capabilities are temporary authorizations.
    """

    def __init__(self):
        self.capabilities: dict[UUID, list[Capability]] = {}

    def grant_capability(
        self, task_id: UUID, capability_type: CapabilityType, **metadata
    ) -> Capability:
        """Grant a capability for a task."""
        capability = Capability(
            type=capability_type, task_id=task_id, metadata=metadata
        )
        if task_id not in self.capabilities:
            self.capabilities[task_id] = []
        self.capabilities[task_id].append(capability)
        return capability

    def get_capabilities(self, task_id: UUID) -> list[Capability]:
        """Get all valid capabilities for a task."""
        if task_id not in self.capabilities:
            return []
        return [cap for cap in self.capabilities[task_id] if cap.is_valid()]

    def has_capability(self, task_id: UUID, capability_type: CapabilityType) -> bool:
        """Check if task has a specific capability."""
        caps = self.get_capabilities(task_id)
        return any(cap.type == capability_type for cap in caps)

    def revoke_all(self, task_id: UUID) -> None:
        """Revoke all capabilities for a task."""
        if task_id in self.capabilities:
            self.capabilities[task_id].clear()


class PolicyGuardian:
    """
    Enforces policies and authorizes execution.
    Authority belongs to the Guardian, not to agents.
    """

    def __init__(self, rules: list[PolicyRule] | None = None):
        self.rules = rules or DefaultPolicies.create_default_rules()
        self.decisions: dict[UUID, PolicyDecision] = {}

    def evaluate_execution(
        self, execution: Execution, context: dict | None = None
    ) -> tuple[PolicyDecision, str | None]:
        """
        Evaluate whether an execution should proceed.

        Returns:
            Tuple of (decision, reason)
        """
        context = context or {}
        # In MVP, check for matching rules and evaluate them
        for rule in self.rules:
            # Simple evaluation: for MVP, we approve most things except write operations
            decision = rule.evaluate(context)
            if decision != PolicyDecision.APPROVED:
                reason = f"Policy '{rule.name}': {rule.description}"
                return decision, reason

        return PolicyDecision.APPROVED, None

    def authorize_execution(self, execution: Execution) -> bool:
        """
        Final authorization decision.
        """
        decision, _ = self.evaluate_execution(execution)
        return decision == PolicyDecision.APPROVED


class Kernel:
    """
    The root of trust.

    The Kernel is responsible for:
    - policy enforcement (via Guardian)
    - capability management (via Manager)
    - execution authorization
    - audit logging (via Logger)
    - task orchestration
    """

    def __init__(self):
        self.guardian = PolicyGuardian()
        self.capability_manager = CapabilityManager()
        self.audit_logger = AuditLogger()
        self.executions: dict[UUID, Execution] = {}

    def submit_execution(self, task: Task) -> Execution | None:
        """
        Submit a task for execution.

        Returns:
            Execution if authorized, None if denied
        """
        execution = Execution(task=task)

        # Step 1: Policy evaluation
        decision, reason = self.guardian.evaluate_execution(execution)
        self.audit_logger.log_execution_start(execution, decision, reason)

        if decision != PolicyDecision.APPROVED:
            execution.state = ExecutionState.FAILED
            execution.error = f"Execution denied: {reason}"
            return None

        # Step 2: Grant capabilities
        self.capability_manager.grant_capability(
            task.id, CapabilityType.PYTHON_EXECUTE
        )

        # Step 3: Track execution
        self.executions[execution.id] = execution
        execution.state = ExecutionState.PENDING

        return execution

    def report_execution_result(
        self, execution_id: UUID, state: ExecutionState, result: str | None = None, error: str | None = None
    ) -> None:
        """Report execution result."""
        if execution_id in self.executions:
            execution = self.executions[execution_id]
            execution.state = state
            execution.result = result
            execution.error = error
            self.audit_logger.log_execution_result(execution, state)

    def get_execution(self, execution_id: UUID) -> Execution | None:
        """Retrieve execution by ID."""
        return self.executions.get(execution_id)

    def get_audit_logs(self, execution_id: UUID | None = None) -> list[AuditLog]:
        """Retrieve audit logs."""
        return self.audit_logger.get_logs(execution_id)
