from typing import Any, Dict, List, Optional

from models.core_entities import ExecutionStep, Task
from managers.audit_logger import audit_logger

from ai_kernel._logging import manager_logger

class TaskExecutor:
    """
    Responsible for invoking approved tools and executing authorized functions.
    Adheres to RFC-0010 (Execution Model) and Article 3 of the Constitution.
    
    The Executor SHALL NOT:
    - modify policy
    - modify capabilities
    - bypass authorization
    """
    def __init__(self):
        self.tools: Dict[str, Any] = {}  # Registry of available tools
        manager_logger.info("TaskExecutor initialized: Ready for execution.")
    
    def register_tool(self, name: str, tool_instance: Any) -> None:
        """Registers a tool for use by the executor."""
        self.tools[name] = tool_instance
        audit_logger.log(
            source_component="TaskExecutor",
            severity="INFO",
            message=f"Tool registered: {name}",
            related_ids=[]
        )
    
    def execute_task(self, task: Task, context: Dict[str, Any]) -> List[ExecutionStep]:
        """
        Executes a given task using registered tools.
        
        Args:
            task: The Task object to execute
            context: Execution context including authorized capabilities
            
        Returns:
            List of ExecutionStep results
        """
        manager_logger.info(f"Starting task: {task.task_id}")
        audit_logger.log(
            source_component="TaskExecutor",
            severity="INFO",
            message=f"Task execution started: {task.task_id}",
            related_ids=[task.task_id]
        )
        
        execution_steps: List[ExecutionStep] = []
        
        # Simplified execution logic for MVP
        # In a real system, this would iterate through required tool invocations
        for capability in task.required_capabilities:
            if capability not in context.get('granted_capabilities', []):
                manager_logger.warning(f"Capability '{capability}' not in granted capabilities.")
                audit_logger.log(
                    source_component="TaskExecutor",
                    severity="WARNING",
                    message=f"Capability not granted: {capability}",
                    related_ids=[task.task_id]
                )
                continue
            
            # Simulate tool execution
            step = ExecutionStep(
                tool_name=capability,
                input_params=context,
                actual_output=f"Simulated output for {capability}"
            )
            execution_steps.append(step)
            manager_logger.info(f"Executed: {capability}")
        
        audit_logger.log(
            source_component="TaskExecutor",
            severity="INFO",
            message=f"Task execution completed: {task.task_id} ({len(execution_steps)} steps)",
            related_ids=[task.task_id]
        )
        
        return execution_steps

# Factory function for lazy initialization
_task_executor_instance = None

def get_task_executor() -> TaskExecutor:
    """Get the singleton TaskExecutor instance."""
    global _task_executor_instance
    if _task_executor_instance is None:
        _task_executor_instance = TaskExecutor()
    return _task_executor_instance

# Backward compatibility alias
task_executor = get_task_executor()
