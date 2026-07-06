"""
Ollama executor for AI-powered code generation.
"""

from __future__ import annotations

import ollama

from ai_kernel.executor.base import Executor
from ai_kernel.kernel.core import Kernel
from ai_kernel.model.execution import Execution, ExecutionState


class OllamaExecutor(Executor):
    """
    Executor that uses Ollama LLM to generate and execute code
    from natural language prompts.
    """

    def __init__(
        self,
        model: str = "qwen3.5:4b",
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url

    def execute(self, execution: Execution, kernel: Kernel) -> None:
        """Execute a task using Ollama LLM to generate code."""
        try:
            if execution.state == ExecutionState.CANCELLED:
                raise RuntimeError("Execution has been cancelled")

            execution.state = ExecutionState.RUNNING
            kernel.report_execution_result(
                execution.id, ExecutionState.RUNNING
            )

            # Get the natural language objective
            objective = execution.task.objective

            # Generate code using Ollama
            result = self._generate_with_ollama(objective)

            kernel.report_execution_result(
                execution.id, ExecutionState.COMPLETED, result=result
            )

        except Exception as exc:
            kernel.report_execution_result(
                execution.id,
                ExecutionState.FAILED,
                error=str(exc),
            )

    def _generate_with_ollama(self, prompt: str) -> str:
        """Generate code using Ollama directly."""
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"""Generate Python code to accomplish the following task:
{prompt}

Respond ONLY with the Python code, no explanations. The code should be complete and runnable.""",
                }
            ],
        )
        return response["message"]["content"]