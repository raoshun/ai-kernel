from typing import List, Dict, Any

from src.models.core_entities import Goal, Task
from src.managers.audit_logger import audit_logger

from ai_kernel._logging import manager_logger

class Planner:
    """
    Responsible for goal decomposition and task planning.
    Adheres to RFC-0001 (Architecture) and Article 3 of the Constitution.
    
    The Planner SHALL NOT:
    - execute tools
    - grant permissions
    - enforce policies
    """
    def __init__(self):
        manager_logger.info("Planner initialized: Ready for planning.")
    
    def create_plan(self, goal: Goal) -> List[Task]:
        """
        Decomposes a Goal into a sequence of Tasks.
        
        Args:
            goal: The Goal object to decompose
            
        Returns:
            List of Task objects forming the execution plan
        """
        manager_logger.info(f"Creating plan for goal: {goal.goal_id}")
        audit_logger.log(
            source_component="Planner",
            severity="INFO",
            message=f"Planning started for goal: {goal.goal_id}",
            related_ids=[goal.goal_id]
        )
        
        tasks: List[Task] = []
        
        # Simplified planning logic for MVP
        # In a real system, this would use LLM reasoning to decompose the goal
        if "report" in goal.description.lower():
            tasks.append(Task(
                task_id=f"{goal.goal_id}_collect_data",
                description="Collect required data for report",
                required_capabilities=["filesystem.read"],
                dependencies=[]
            ))
            tasks.append(Task(
                task_id=f"{goal.goal_id}_generate",
                description="Generate report content",
                required_capabilities=["llm.generate"],
                dependencies=[f"{goal.goal_id}_collect_data"]
            ))
            tasks.append(Task(
                task_id=f"{goal.goal_id}_save",
                description="Save report to filesystem",
                required_capabilities=["filesystem.write"],
                dependencies=[f"{goal.goal_id}_generate"]
            ))
        else:
            # Generic task for unknown goals
            tasks.append(Task(
                task_id=f"{goal.goal_id}_execute",
                description=f"Execute goal: {goal.description}",
                required_capabilities=["generic.execute"],
                dependencies=[]
            ))
        
        manager_logger.info(f"Generated {len(tasks)} tasks for goal: {goal.goal_id}")
        audit_logger.log(
            source_component="Planner",
            severity="INFO",
            message=f"Planning completed: {len(tasks)} tasks generated",
            related_ids=[goal.goal_id]
        )
        
        return tasks

    def estimate_risk(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Provides a basic risk assessment for the plan.
        This is a placeholder for more sophisticated risk analysis.
        
        Returns:
            Dictionary containing risk level and flags
        """
        # Simple heuristic: more tasks = higher complexity/risk
        risk_level = "LOW"
        if len(tasks) > 5:
            risk_level = "MEDIUM"
        if len(tasks) > 10:
            risk_level = "HIGH"
            
        return {
            "risk_level": risk_level,
            "task_count": len(tasks),
            "requires_human_approval": risk_level == "HIGH"
        }

# Singleton access
planner = Planner()
