from crewai import Agent, Crew, LLM, Task as CrewTask

from ai_kernel.executor.base import Executor
from ai_kernel.model.task import Task


class CrewAIExecutor(Executor):

    def __init__(
        self,
        model: str = "ollama/qwen3.5:4b",
        base_url: str = "http://localhost:11434",
    ):
        self.llm = LLM(
            model=model,
            base_url=base_url,
        )

    def execute(self, task: Task) -> str:

        agent = Agent(
            role="Executor",
            goal="Complete the given task.",
            backstory="You are the execution engine of AI Kernel.",
            llm=self.llm,
            verbose=False,
        )

        crew_task = CrewTask(
            description=task.objective,
            expected_output="Task result",
            agent=agent,
        )

        crew = Crew(
            agents=[agent],
            tasks=[crew_task],
            verbose=False,
        )

        return str(crew.kickoff())
