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
from src.models.core_entities import Task, ExecutionStep
from src.managers.audit_logger import audit_logger


class Reviewer:
    """
    Validates execution results and provides feedback for improvement.
    """
    def __init__(self):
        print("--> Reviewer Initialized: Ready for result validation.")
    
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
        print(f"[REVIEWER] Reviewing task: {task.task_id}")
        
        validation_result = {
            "task_id": task.task_id,
            "status": "SUCCESS",
            "steps_executed": len(execution_steps),
            "issues": [],
            "recommendations": []
        }
        
        # Check if any steps were executed
        if len(execution_steps) == 0:
            validation_result["status"] = "WARNING"
            validation_result["issues"].append("No execution steps completed")
            validation_result["recommendations"].append(
                "Verify that required capabilities were granted"
            )
        
        # Check each execution step for issues
        for step in execution_steps:
            if not step.actual_output:
                validation_result["status"] = "WARNING"
                validation_result["issues"].append(
                    f"Tool '{step.tool_name}' produced no output"
                )
            
            # Check for common error indicators in output
            if step.actual_output and any(
                err in step.actual_output.lower() 
                for err in ["error", "failed", "exception"]
            ):
                validation_result["status"] = "FAILED"
                validation_result["issues"].append(
                    f"Tool '{step.tool_name}' reported an error"
                )
        
        # Check task dependencies
        if task.dependencies:
            validation_result["recommendations"].append(
                "Task has dependencies - ensure they completed successfully"
            )
        
        # Log the review
        audit_logger.log(
            source_component="Reviewer",
            severity="INFO" if validation_result["status"] == "SUCCESS" else "WARNING",
            message=f"Review completed for task {task.task_id}: {validation_result['status']}",
            related_ids=[task.task_id]
        )
        
        return validation_result
    
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
        print(f"[REVIEWER] Reviewing plan execution: {len(tasks)} tasks")
        
        task_reviews = []
        success_count = 0
        warning_count = 0
        failed_count = 0
        
        for task, steps in zip(tasks, execution_results):
            review = self.review_task_execution(task, steps)
            task_reviews.append(review)
            
            if review["status"] == "SUCCESS":
                success_count += 1
            elif review["status"] == "WARNING":
                warning_count += 1
            else:
                failed_count += 1
        
        overall_status = "SUCCESS"
        if failed_count > 0:
            overall_status = "FAILED"
        elif warning_count > 0:
            overall_status = "PARTIAL"
        
        return {
            "overall_status": overall_status,
            "total_tasks": len(tasks),
            "successful_tasks": success_count,
            "warning_tasks": warning_count,
            "failed_tasks": failed_count,
            "task_reviews": task_reviews,
            "overall_recommendations": self._generate_overall_recommendations(
                overall_status, success_count, warning_count, failed_count
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
            recommendations.append("Consider optimizing workflow for better performance")
        
        return recommendations


# Singleton access
reviewer = Reviewer()
