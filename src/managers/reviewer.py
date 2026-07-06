"""
Reviewer - Validates execution results and recommends improvements.

Adheres to RFC-0001 (Architecture) and Article 10 of the Constitution.

The Reviewer is responsible for:
- validating execution results
- detecting failures
- recommending improvements

The Reviewer SHALL NOT execute tools directly.
"""
from typing import List, Dict, Any, Optional

from models.core_entities import Task, ExecutionStep
from managers.audit_logger import audit_logger
from managers.validation_helper import ExecutionValidator

from ai_kernel._logging import manager_logger


class Reviewer:
    """
    Validates execution results and provides feedback for improvement.
    Delegates validation logic to ExecutionValidator.
    """
    def __init__(self):
        manager_logger.info("Reviewer initialized: Ready for result validation.")
    
    def review_task_execution(
        self, 
        task: Task, 
        execution_steps: List[ExecutionStep]
    ) -> Dict[str, Any]:
        """
        Reviews the execution of a single task.
        
        Args:
            task: The executed task
            execution_steps: List of execution steps taken
            
        Returns:
            Dictionary containing validation results and recommendations
        """
        manager_logger.info(f"Reviewing task: {task.task_id}")
        
        # Delegate validation to ExecutionValidator
        step_validation = ExecutionValidator.validate_execution_steps(execution_steps)
        
        validation_result = {
            "task_id": task.task_id,
            "status": ExecutionValidator.classify_overall_status(
                step_validation['error_steps'],
                step_validation['warning_steps'],
                step_validation['successful_steps']
            ),
            "steps_executed": step_validation['total_steps'],
            "issues": step_validation['issues'],
            "recommendations": self._generate_recommendations(
                task, step_validation
            )
        }
        
        # Log the review
        audit_logger.log(
            source_component="Reviewer",
            severity="INFO" if validation_result["status"] == "SUCCESS" else "WARNING",
            message=f"Review completed for task {task.task_id}: {validation_result['status']}",
            related_ids=[task.task_id]
        )
        
        return validation_result
    
    def _generate_recommendations(
        self,
        task: Task,
        validation: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if validation['error_steps'] > 0:
            recommendations.append("Review failed steps - check capability permissions")
        
        if validation['warning_steps'] > 0:
            recommendations.append("Investigate warnings in execution output")
        
        if validation['total_steps'] == 0:
            recommendations.append("No steps executed - verify required capabilities were granted")
        
        if task.dependencies:
            recommendations.append("Verify task dependencies completed successfully")
        
        return recommendations
    
    def review_plan_execution(
        self, 
        tasks: List[Task], 
        execution_results: List[List[ExecutionStep]]
    ) -> Dict[str, Any]:
        """
        Reviews the execution of an entire plan.
        
        Args:
            tasks: List of executed tasks
            execution_results: List of execution step lists per task
            
        Returns:
            Dictionary containing overall review results
        """
        manager_logger.info(f"Reviewing plan execution: {len(tasks)} tasks")
        
        task_reviews = []
        error_count = 0
        warning_count = 0
        success_count = 0
        
        for task, steps in zip(tasks, execution_results):
            review = self.review_task_execution(task, steps)
            task_reviews.append(review)
            
            if review["status"] == "SUCCESS":
                success_count += 1
            elif review["status"] == "PARTIAL":
                warning_count += 1
            else:
                error_count += 1
        
        overall_status = ExecutionValidator.classify_overall_status(
            error_count, warning_count, success_count
        )
        
        return {
            "overall_status": overall_status,
            "total_tasks": len(tasks),
            "successful_tasks": success_count,
            "warning_tasks": warning_count,
            "failed_tasks": error_count,
            "task_reviews": task_reviews,
            "overall_recommendations": self._generate_overall_recommendations(
                overall_status, success_count, warning_count, error_count
            )
        }
    
    def _generate_overall_recommendations(
        self, 
        status: str, 
        success: int, 
        warnings: int, 
        failures: int
    ) -> List[str]:
        """Generates overall recommendations based on execution summary."""
        recommendations = []
        
        if status == "FAILED":
            recommendations.append("Review failed tasks and address root causes")
            recommendations.append("Check capability permissions and tool availability")
        elif status == "PARTIAL":
            recommendations.append("Investigate tasks with warnings")
            recommendations.append("Review logs for detailed error information")
        else:
            recommendations.append("Execution completed successfully")
        
        return recommendations


# Factory function for lazy initialization
_reviewer_instance = None

def get_reviewer() -> Reviewer:
    """Get the singleton Reviewer instance."""
    global _reviewer_instance
    if _reviewer_instance is None:
        _reviewer_instance = Reviewer()
    return _reviewer_instance

# Backward compatibility alias
reviewer = get_reviewer()
