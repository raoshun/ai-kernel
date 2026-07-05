"""
RFC-0003/0004: Policy Model

A Policy is a deterministic rule governing system behavior.
Policies are enforced by the Kernel and SHALL NOT depend solely on LLM reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from ai_kernel.capability.model import CapabilityType


class PolicyDecision(str, Enum):
    """Policy evaluation decision."""

    APPROVED = "approved"
    DENIED = "denied"
    REQUIRES_REVIEW = "requires_review"


@dataclass
class PolicyRule:
    """
    A single policy rule.

    A rule determines whether a capability request should be approved, denied,
    or escalated for review.
    """

    name: str
    description: str
    capability_type: CapabilityType
    evaluator: Callable[[dict], PolicyDecision]

    def evaluate(self, context: dict) -> PolicyDecision:
        """Evaluate this rule against a context."""
        return self.evaluator(context)


class DefaultPolicies:
    """Default policies for MVP."""

    @staticmethod
    def create_default_rules() -> list[PolicyRule]:
        """Create a default set of policies."""
        return [
            PolicyRule(
                name="shell_execute_allowed",
                description="Allow shell execution in MVP",
                capability_type=CapabilityType.SHELL_EXECUTE,
                evaluator=lambda ctx: PolicyDecision.APPROVED,
            ),
            PolicyRule(
                name="filesystem_read_allowed",
                description="Allow filesystem read operations",
                capability_type=CapabilityType.FILESYSTEM_READ,
                evaluator=lambda ctx: PolicyDecision.APPROVED,
            ),
            PolicyRule(
                name="filesystem_write_allowed",
                description="Allow filesystem write operations in MVP",
                capability_type=CapabilityType.FILESYSTEM_WRITE,
                evaluator=lambda ctx: PolicyDecision.APPROVED,
            ),
            PolicyRule(
                name="python_execute_allowed",
                description="Allow Python execution in MVP",
                capability_type=CapabilityType.PYTHON_EXECUTE,
                evaluator=lambda ctx: PolicyDecision.APPROVED,
            ),
            PolicyRule(
                name="git_read_allowed",
                description="Allow Git read operations",
                capability_type=CapabilityType.GIT_READ,
                evaluator=lambda ctx: PolicyDecision.APPROVED,
            ),
        ]
