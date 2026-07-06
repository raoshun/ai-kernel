"""
AI Kernel Core - The trusted control plane of the entire system.

Adheres to RFC-0013 (Kernel Model) and Article 4 of the Constitution.

The Kernel is responsible for:
- policy enforcement
- capability management
- execution authorization
- audit logging
- task orchestration
"""
from typing import Dict, List, Optional, Any

from src.models.core_entities import Goal, Task, Authority, Capability
from src.managers.planner import planner
from src.managers.policy_engine import policy_engine
from src.managers.capability_manager import capability_manager
from src.managers.task_executor import task_executor
from src.managers.audit_logger import audit_logger

from ai_kernel._logging import kernel_logger


class Kernel:
    """
    The central orchestration component.
    Implements the execution lifecycle defined in RFC-0001.
    """
    def __init__(self, user_authority: Authority):
        self.user_authority = user_authority
        self.state: Dict[str, Any] = {}
        
        kernel_logger.info(f"Kernel initialized for user: {user_authority.principal_id}")
        audit_logger.log(
            source_component="Kernel",
            severity="INFO",
            message=f"Kernel initialized for user: {user_authority.principal_id}",
            related_ids=[]
        )
    
    def process_goal(self, goal: Goal) -> Dict[str, Any]:
        """
        Main entry point for processing a user goal.
        Implements the full execution lifecycle.
        """
        kernel_logger.info(f"Processing goal: {goal.goal_id}")
        
        audit_logger.log(
            source_component="Kernel",
            severity="INFO",
            message=f"Goal received: {goal.goal_id}",
            related_ids=[goal.goal_id]
        )
        
        # Phase 1: Planning
        tasks = planner.create_plan(goal)
        kernel_logger.info(f"Planning complete: {len(tasks)} tasks generated")
        
        # Phase 2: Risk Assessment
        risk_assessment = planner.estimate_risk(tasks)
        kernel_logger.info(f"Risk Assessment: {risk_assessment['risk_level']}")
        
        if risk_assessment.get("requires_human_approval"):
            audit_logger.log(
                source_component="Kernel",
                severity="WARNING",
                message=f"High risk detected for goal: {goal.goal_id}",
                related_ids=[goal.goal_id]
            )
            return {
                "status": "REQUIRES_APPROVAL",
                "risk": risk_assessment,
                "goal_id": goal.goal_id
            }
        
        # Phase 3: Policy Evaluation & Capability Grant
        authorized_capabilities = self._authorize_capabilities(tasks)
        kernel_logger.info(f"Authorized capabilities: {len(authorized_capabilities)} granted")
        
        # Phase 4: Execution
        execution_results = self._execute_tasks(tasks, authorized_capabilities, goal.goal_id)
        
        # Phase 5: Audit Logging (already done throughout)
        kernel_logger.info(f"Goal processing complete: {goal.goal_id}")
        
        return {
            "status": "COMPLETED",
            "goal_id": goal.goal_id,
            "tasks_executed": len(execution_results),
            "risk_assessment": risk_assessment
        }
    
    def _authorize_capabilities(self, tasks: List[Task]) -> List[str]:
        """
        Evaluates policy and grants capabilities for the given tasks.
        """
        authorized = []
        
        for task in tasks:
            for cap_name in task.required_capabilities:
                cap = capability_manager.get_capability(cap_name)
                if cap and policy_engine.check_permission(self.user_authority, cap):
                    if cap_name not in authorized:
                        authorized.append(cap_name)
                else:
                    audit_logger.log(
                        source_component="Kernel",
                        severity="WARNING",
                        message=f"Capability denied: {cap_name} for task {task.task_id}",
                        related_ids=[task.task_id]
                    )
        
        return authorized
    
    def _execute_tasks(self, tasks: List[Task], capabilities: List[str], goal_id: str) -> List[Any]:
        """
        Executes tasks using the authorized capabilities.
        """
        results = []
        context = {
            "goal_id": goal_id,
            "granted_capabilities": capabilities
        }
        
        for task in tasks:
            result = task_executor.execute_task(task, context)
            results.append(result)
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Returns current kernel status."""
        return {
            "user": self.user_authority.principal_id,
            "registered_capabilities": len(capability_manager.capabilities),
            "audit_records": len(audit_logger.get_all_records())
        }


def create_kernel(user_id: str, role: str = "USER") -> Kernel:
    """Factory function to create a Kernel instance."""
    authority = Authority(principal_id=user_id, role=role)
    return Kernel(authority)
