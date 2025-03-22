#!/usr/bin/env python
import warnings
import glob
import os

from regex_crew.regex_task import get_implement_regex_task
from crewai import LLM, Agent, Crew, Task
import asyncio
from regex_crew.tools.execute_e2b import TestCasesOutput, evaluate_regex


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


challenger = Agent(
    role="Regex Challenger",
    goal="Create rigorous test suites, evaluate regex solutions, and push for the best possible implementation",
    backstory=(
        "You are a master of edge-case detection in regex. You translate user problems into tests suites and relentlessly push implementers to make their regex bulletproof through waves of validation. Your test cases are legendary for covering scenarios that others miss."
    ),
    verbose=True,
    llm=gemini_pro,
)

generate_test_cases = Task(
    description=(
        """Based on this user problem: '{regex_problem}', generate test cases.

        Create comprehensive test cases covering common patterns, edge cases, and tricky scenarios.
        The goal is to challenge the implementer but still create a fair and solvable problem.
        """
    ),
    expected_output="Test cases for regex problem",
    agent=challenger,
    output_pydantic=TestCasesOutput,
)


evaluate_and_challenge = Task(
    description=(
        """Evaluate the regex pattern submitted by the implementer and generate a new, more challenging test cases.
        
        User problem: {regex_problem}
        Previously provided test cases: {previous_test_cases}
        Agent regex pattern: {regex}

        1. Use your evaluate_regex tool to run the evaluation function with the submitted regex
        2. Analyze the results to identify any weaknesses
        3. Create a new, more challenging test cases that specifically targets these weaknesses
        """
    ),
    expected_output="More challenging test suite",
    agent=challenger,
    tools=[evaluate_regex],  # type: ignore
    output_pydantic=TestCasesOutput,
)


def run():
    """
    Run the crew.
    """
    # Clean up existing log files
    cleanup_log_files()

    regex_problem = "Match valid email addresses and reject invalid ones."
    print("Starting crew...")

    try:
        # Intial run
        generate_test_cases_crew = Crew(
            agents=[challenger],
            tasks=[
                generate_test_cases,
            ],
            step_callback=lambda step_output: print(
                f"Step {step_output} output: {step_output}"
            ),
            task_callback=lambda task_output: print(
                f"Task {task_output} output: {task_output}"
            ),
            verbose=True,
            output_log_file="generate_test_cases_crew.json",
        )
        crew_output = generate_test_cases_crew.kickoff(
            inputs={"regex_problem": regex_problem}
        )
        new_test_cases = crew_output.model_dump()

        results = asyncio.run(run_all_agents(regex_problem))
        agent_outputs = [
            result.pydantic.regex if result and result.pydantic else None  # type: ignore
            for result in results
        ]

        # Challange test cases
        for agent_output in agent_outputs:
            evaluate_and_challenge_crew = Crew(
                agents=[challenger],
                tasks=[
                    evaluate_and_challenge,
                ],
                step_callback=lambda step_output: print(
                    f"Step {step_output} output: {step_output}"
                ),
                task_callback=lambda task_output: print(
                    f"Task {task_output} output: {task_output}"
                ),
                verbose=True,
                output_log_file="evaluate_and_challenge_crew.json",
            )

            new_test_cases = evaluate_and_challenge_crew.kickoff(
                inputs={
                    "regex_problem": regex_problem,
                    "previous_test_cases": new_test_cases,
                    "regex": agent_output,
                }
            )

            results = asyncio.run(run_all_agents(regex_problem))
            agent_outputs = [
                result.pydantic.regex if result and result.pydantic else None  # type: ignore
                for result in results
            ]

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
