#!/usr/bin/env python
import warnings
import glob
import os

from regex_crew.regex_task import get_implement_regex_task
from crewai import LLM, Agent, Crew
import asyncio


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def cleanup_log_files():
    """Remove all existing regex crew log files."""
    for log_file in glob.glob("regex_crew_*.json"):
        try:
            os.remove(log_file)
        except OSError as e:
            print(f"Error removing log file {log_file}: {e}")


gemini_flash = LLM(
    model="gemini/gemini-2.0-flash",
)

gemini_pro = LLM(
    model="gemini/gemini-2.0-pro-exp-02-05",
)

agents = [
    Agent(
        role="1. Simple Regex Engineer",
        goal="Write the perfect regex pattern that passes all test cases with 100% accuracy",
        backstory=(
            "You're a seasoned regex builder with deep understanding of pattern matching. "
            "You study test suites carefully and respond with precise regex expressions to pass them all. "
            "Your patterns are elegant, efficient, and robust against edge cases."
        ),
        llm=gemini_flash,
    ),
    Agent(
        role="2. Simple Regex Engineer",
        goal="Write the perfect regex pattern that passes all test cases with 100% accuracy",
        backstory=(
            "You're a seasoned regex builder with deep understanding of pattern matching. "
            "You study test suites carefully and respond with precise regex expressions to pass them all. "
            "Your patterns are elegant, efficient, and robust against edge cases."
        ),
        llm=gemini_flash,
    ),
    Agent(
        role="3. Simple Regex Engineer",
        goal="Write the perfect regex pattern that passes all test cases with 100% accuracy",
        backstory=(
            "You're a seasoned regex builder with deep understanding of pattern matching. "
            "You study test suites carefully and respond with precise regex expressions to pass them all. "
            "Your patterns are elegant, efficient, and robust against edge cases."
        ),
        llm=gemini_flash,
    ),
    Agent(
        role="4. Drunk Regex Engineer",
        goal="Write the perfect regex pattern that passes all test cases with 100% accuracy",
        backstory=(
            "You're a regex wizard who's had one too many drinks at the office party. "
            "Your knowledge of regex is still intact, but your explanations are slurred and your thought process is erratic. "
            "You occasionally mix up symbols and have to correct yourself mid-pattern. "
            "Despite your inebriated state, you're determined to solve the problem, even if your path to the solution is a bit wobbly."
        ),
        llm=gemini_flash,
    ),
]


def run():
    """
    Run the crew.
    """
    # Clean up existing log files
    cleanup_log_files()

    regex_problem = "Match valid email addresses and reject invalid ones."
    print("Starting crew...")

    try:
        results = asyncio.run(run_all_agents(regex_problem))
        print(results)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


async def run_all_agents(regex_problem):
    tasks = [
        async_crew_execution(agent, i, regex_problem) for i, agent in enumerate(agents)
    ]
    return await asyncio.gather(*tasks)


def format_step_output(step_output):
    """Format step output for logging based on its type."""
    if hasattr(step_output, "thought") and hasattr(step_output, "output"):
        # This is an AgentFinish
        return f"🤖 Agent's Answer: {step_output.output}\n"
    else:
        # Fallback for unknown types
        return f"Unknown output type: {str(step_output)}"


async def async_crew_execution(agent, name, regex_problem):
    regex_crew = Crew(
        agents=[agent],
        tasks=[get_implement_regex_task(agent)],
        step_callback=lambda step_output: print(format_step_output(step_output)),
        task_callback=lambda task_output: print(f"\n📋 Task Complete: {task_output}\n"),
        output_log_file=f"regex_crew_{name}.json",
    )
    result = await regex_crew.kickoff_async(inputs={"regex_problem": regex_problem})
    return result
