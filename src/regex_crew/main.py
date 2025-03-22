#!/usr/bin/env python
import os
import warnings

from crewai import Crew

from regex_crew.crew import (
    challenger,
    evaluate_and_challenge_round1,
    evaluate_and_challenge_round2,
    final_evaluation,
    generate_test_suite_round1,
    implement_regex_final,
    implement_regex_round1,
    implement_regex_round2,
    implementer,
)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    # Remove the output log file if it exists
    log_file = "regex_crew.json"
    if os.path.exists(log_file):
        os.remove(log_file)

    inputs = {"regex_problem": "Match valid email addresses and reject invalid ones."}

    print("Starting crew...")

    try:
        code_execution_crew = Crew(
            agents=[challenger, implementer],
            tasks=[
                generate_test_suite_round1,
                implement_regex_round1,
                evaluate_and_challenge_round1,
                implement_regex_round2,
                evaluate_and_challenge_round2,
                implement_regex_final,
                final_evaluation,
            ],
            step_callback=lambda step_output: print(
                f"Step {step_output} output: {step_output}"
            ),
            task_callback=lambda task_output: print(
                f"Task {task_output} output: {task_output}"
            ),
            verbose=True,
            output_log_file=log_file,
        )
        result = code_execution_crew.kickoff(inputs)
        print(result)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
