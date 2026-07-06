from __future__ import annotations

from abc import ABC, abstractmethod

from ai_kernel.model.task import Task


class Executor(ABC):

    @abstractmethod
    def execute(self, task: Task) -> str:
        """Execute a task."""
        raise NotImplementedError
