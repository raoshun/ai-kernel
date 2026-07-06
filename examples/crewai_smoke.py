from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="ollama/qwen3.5:4b",
    base_url="http://localhost:11434",
)

agent = Agent(
    role="Assistant",
    goal="Answer the user's question.",
    backstory="A helpful AI assistant.",
    llm=llm,
    verbose=True,
)

task = Task(
    description="Say hello in one sentence.",
    expected_output="A short greeting.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
)

result = crew.kickoff()

print("\n===== RESULT =====")
print(result)
