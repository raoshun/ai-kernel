"""
Executor implementations for running tasks.

Tools perform actions but never make decisions.
Executors respect capability authorization from the Kernel.
"""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from uuid import UUID

from ai_kernel.capability.model import CapabilityType
from ai_kernel.kernel.core import Kernel
from ai_kernel.model.execution import Execution, ExecutionState
from ai_kernel.model.task import Task


class Executor(ABC):
    """Base executor interface."""

    @abstractmethod
    def execute(self, execution: Execution, kernel: Kernel) -> None:
        """Execute a task."""
        pass


class BasicExecutor(Executor):
    """
    Basic executor that can run Python code and shell commands.

    This executor checks capabilities before executing.
    """

    def execute(self, execution: Execution, kernel: Kernel) -> None:
        """Execute a task if authorized."""
        try:
            # Check if we have Python execution capability
            if not kernel.capability_manager.has_capability(
                execution.task.id, CapabilityType.PYTHON_EXECUTE
            ):
                raise PermissionError("Python execution capability not granted")

            # Execute the task objective as Python code
            result = self._execute_python(execution.task.objective)

            # Report success
            kernel.report_execution_result(
                execution.id, ExecutionState.COMPLETED, result=result
            )

        except Exception as e:
            # Report failure
            kernel.report_execution_result(
                execution.id,
                ExecutionState.FAILED,
                error=str(e),
            )

    def _execute_python(self, code: str) -> str:
        """Execute Python code safely."""
        try:
            local_context: dict = {}
            exec(code, {"__builtins__": __builtins__}, local_context)
            return "Execution completed successfully"
        except Exception as e:
            raise RuntimeError(f"Python execution error: {e}")


class ShellExecutor(Executor):
    """
    Executor for shell commands.
    """

    def execute(self, execution: Execution, kernel: Kernel) -> None:
        """Execute a shell command if authorized."""
        try:
            # Check if we have shell execution capability
            if not kernel.capability_manager.has_capability(
                execution.task.id, CapabilityType.SHELL_EXECUTE
            ):
                raise PermissionError("Shell execution capability not granted")

            # Execute the command
            result = self._execute_shell(execution.task.objective)

            # Report success
            kernel.report_execution_result(
                execution.id, ExecutionState.COMPLETED, result=result
            )

        except Exception as e:
            # Report failure
            kernel.report_execution_result(
                execution.id,
                ExecutionState.FAILED,
                error=str(e),
            )

    def _execute_shell(self, command: str) -> str:
        """Execute a shell command safely."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return f"Command failed: {result.stderr}"
            return result.stdout
        except subprocess.TimeoutExpired:
            raise RuntimeError("Command execution timed out")
        except Exception as e:
            raise RuntimeError(f"Shell execution error: {e}")


class ExecutorRegistry:
    """Registry of available executors."""

    def __init__(self):
        self.executors: dict[str, Executor] = {
            "basic": BasicExecutor(),
            "shell": ShellExecutor(),
            "python": BasicExecutor(),  # Default to basic for Python
        }

    def execute(
        self,
        executor_name: str,
        execution: Execution,
        kernel: Kernel,
    ) -> None:
        """Execute using a registered executor."""
        executor = self.executors.get(executor_name)
        if not executor:
            raise ValueError(f"Unknown executor: {executor_name}")
        executor.execute(execution, kernel)

    def register(self, name: str, executor: Executor) -> None:
        """Register a new executor."""
        self.executors[name] = executor
