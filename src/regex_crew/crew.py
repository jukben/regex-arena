# pip install crewai e2b-code-interpreter
from crewai.tools import tool
from crewai import Agent, Task, Crew
from regex_crew.tools.execute_e2b import execute_python


# Define the agent
python_executor = Agent(
    role='Python Executor',
    goal='Execute Python code and return the results',
    backstory='You are an expert Python programmer capable of executing code and returning results.',
    tools=[execute_python], # type: ignore
)

# Define the task
execute_task = Task(
    description="Calculate how many r's are in the word 'strawberry'",
    agent=python_executor,
    expected_output="The number of r's in the word 'strawberry'"
)

# Create the crew
code_execution_crew = Crew(
    agents=[python_executor],
    tasks=[execute_task],
    verbose=True,
)

# Run the crew
result = code_execution_crew.kickoff()
print(result)
