from crewai import Agent, Task
from pydantic import BaseModel, Field


class RegexOutput(BaseModel):
    regex: str = Field(..., description="The regex pattern solution")


def get_implement_regex_task(implementer: Agent):
    return Task(
        description=(
            """Create the best possible regex pattern for this problem: '{regex_problem}'

        IMPORTANT: Return ONLY the regex pattern string itself, nothing else. No code, no explanation.
        """
        ),
        expected_output="A regex pattern string",
        agent=implementer,
        output_pydantic=RegexOutput,
    )
