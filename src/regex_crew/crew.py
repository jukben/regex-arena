import os
from crewai import Agent, Task, Crew, Process

from regex_crew.tools.execute_e2b import execute_python

os.environ["OPENAI_API_KEY"] = "your-openai-key"

# User Input (you can turn this into actual user input if needed)
regex_problem = "Match valid email addresses and reject invalid ones."

# Agent 1: Challenger
challenger = Agent(
    role="Regex Challenger",
    goal="Craft rigorous test cases for regex problems, evaluate solutions, and force regex refinement",
    backstory=(
        "You are a master of edge-case detection in regex. You translate user problems into tricky Python test suites "
        "and relentlessly push implementers to make their regex bulletproof through waves of validation."
    ),
    
    tools=[execute_python], # type: ignore
    verbose=True,
)

# Agent 2: Code Implementer
implementer = Agent(
    role="Regex Engineer",
    goal="Write the best regex that can pass rigorous test cases with high accuracy",
    backstory=(
        "You're a seasoned regex builder with deep understanding of pattern matching. "
        "You study test suites carefully and respond with precise regex expressions to pass them all."
    ),
    verbose=True,
    tools=[execute_python], # type: ignore
)


# === TASKS ===

# Round 1: Challenger creates tests
generate_test_suite_round1 = Task(
    description=(
        f"Based on this user problem: '{regex_problem}', generate Python code for test suites.\n"
        "Your output must be valid Python code that includes:\n"
        "1. A variable `test_suite` with two keys: 'valid' and 'invalid' (list of strings)\n"
        "2. A function `evaluate_regex(regex: str)` that compiles the regex and checks the test cases.\n"
        "3. The function should return: {'score': int, 'false_negatives': [...], 'false_positives': [...], 'feedback': str}\n"
        "Be creative in crafting tricky edge cases."
    ),
    expected_output="Python code as described above.",
    agent=challenger
)

# Round 1: Code Implementation
implement_regex_round1 = Task(
    description=(
        "Using the test_suite and evaluate_regex() function provided by the Challenger, "
        "implement the best possible regex for this problem:\n"
        f"'{regex_problem}'\n"
        "Return ONLY the regex string. Make sure it passes the tests."
    ),
    expected_output="A single regex string",
    agent=implementer
)

# Round 1: Evaluation and Challenge Refinement
evaluate_and_challenge_round1 = Task(
    description=(
        "Evaluate the regex returned by the implementer using the `evaluate_regex` function you generated. "
        "If the solution passes, make it harder by improving the test_suite with sneakier edge cases. "
        "Return the updated Python test code for round 2."
    ),
    expected_output="Python code with updated test_suite and evaluate_regex() function.",
    agent=challenger
)

# Round 2: Implement again
implement_regex_round2 = Task(
    description=(
        "Use the newly updated test suite to re-implement a better regex. "
        "Return only the regex string. It must pass this second, harder round."
    ),
    expected_output="Improved regex string.",
    agent=implementer
)

# Round 3: Final challenge
final_challenge = Task(
    description=(
        "This is your final round. Evaluate the regex again. "
        "Make one last set of edge case improvements to the test suite and provide a FINAL evaluation report.\n"
        "Output the final test suite, the final evaluation score, and summarize false positives/negatives."
    ),
    expected_output=(
        "Return a JSON like: {'final_regex': str, 'score': int, "
        "'false_negatives': [...], 'false_positives': [...], 'feedback': str, 'final_test_suite': dict}"
    ),
    agent=challenger
)

# === CREW ===
crew = Crew(
    agents=[challenger, implementer],
    tasks=[
        generate_test_suite_round1,
        implement_regex_round1,
        evaluate_and_challenge_round1,
        implement_regex_round2,
        final_challenge
    ],
    process=Process.sequential
)

# === Run the full regex challenge ===
final_result = crew.kickoff(inputs={
    "regex_problem": regex_problem
})

print("🏁 FINAL RESULT:\n", final_result)
