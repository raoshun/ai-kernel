"""
Risk Assessor - Evaluates operational risk and assigns risk levels.

Adheres to RFC-0001 (Architecture) and Article 2 of the Constitution.

The Risk Assessor is responsible for:
- evaluating operational risk
- assigning risk levels
- recommending mitigations
- providing risk assessment inputs to the Policy Guardian

The Risk Assessor SHALL NOT execute operations.
"""
from typing import List, Dict, Any, Literal

from src.models.core_entities import Task

from ai_kernel._logging import manager_logger


class RiskAssessor:
    """
    Evaluates the risk level of proposed tasks and execution plans.
    """
    def __init__(self):
        manager_logger.info("RiskAssessor initialized: Ready for risk analysis.")
    
    def assess_task_risk(self, task: Task) -> Dict[str, Any]:
        """
        Assesses the risk level of a single task.
        
        Returns:
            Dictionary containing risk level, flags, and recommendations
        """
        risk_factors = []
        risk_level = "LOW"
        
        # Check capability requirements
        for cap in task.required_capabilities:
            if "write" in cap.lower() or "delete" in cap.lower():
                risk_factors.append(f"Write/Delete capability required: {cap}")
                risk_level = "MEDIUM"
            
            if "execute" in cap.lower() or "shell" in cap.lower():
                risk_factors.append(f"Execution capability required: {cap}")
                risk_level = "HIGH"
            
            if "network" in cap.lower() or "http" in cap.lower():
                risk_factors.append(f"Network capability required: {cap}")
                if risk_level != "HIGH":
                    risk_level = "MEDIUM"
        
        # Check task complexity
        if len(task.dependencies) > 3:
            risk_factors.append("High dependency count")
            if risk_level == "LOW":
                risk_level = "MEDIUM"
        
        # Check retry attempts
        if task.max_attempts > 5:
            risk_factors.append("High retry threshold")
        
        return {
            "task_id": task.task_id,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "requires_human_approval": risk_level == "HIGH",
            "mitigations": self._get_mitigations(risk_level)
        }
    
    def assess_plan_risk(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Assesses the overall risk of a plan (collection of tasks).
        
        Returns:
            Dictionary containing overall risk level and per-task assessments
        """
        task_assessments = []
        high_risk_count = 0
        medium_risk_count = 0
        
        for task in tasks:
            assessment = self.assess_task_risk(task)
            task_assessments.append(assessment)
            
            if assessment["risk_level"] == "HIGH":
                high_risk_count += 1
            elif assessment["risk_level"] == "MEDIUM":
                medium_risk_count += 1
        
        # Determine overall plan risk
        overall_risk = "LOW"
        if high_risk_count > 0:
            overall_risk = "HIGH"
        elif medium_risk_count > 0:
            overall_risk = "MEDIUM"
        
        return {
            "overall_risk_level": overall_risk,
            "task_count": len(tasks),
            "high_risk_tasks": high_risk_count,
            "medium_risk_tasks": medium_risk_count,
            "task_assessments": task_assessments,
            "requires_human_approval": overall_risk == "HIGH"
        }
    
    def _get_mitigations(self, risk_level: str) -> List[str]:
        """Provides mitigation recommendations based on risk level."""
        if risk_level == "HIGH":
            return [
                "Require explicit human approval",
                "Limit execution time",
                "Enable sandbox mode",
                "Log all operations in detail"
            ]
        elif risk_level == "MEDIUM":
            return [
                "Enable verbose logging",
                "Set execution timeout",
                "Review output before proceeding"
            ]
        else:
            return ["Standard monitoring"]


# Factory function for lazy initialization
_risk_assessor_instance = None

def get_risk_assessor() -> RiskAssessor:
    """Get the singleton RiskAssessor instance."""
    global _risk_assessor_instance
    if _risk_assessor_instance is None:
        _risk_assessor_instance = RiskAssessor()
    return _risk_assessor_instance

# Backward compatibility alias
risk_assessor = get_risk_assessor()
