from typing import List

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel, Field

from regex_crew.tools.execute_e2b import TestCasesOutput, execute_e2b


class RegexOutput(BaseModel):
    regex: str = Field(..., description="The regex pattern solution")


class FinalEvaluationOutput(BaseModel):
    final_regex: str = Field(
        ...,
        description="The final regex pattern submitted by the Code Implementation Agent",
    )
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="The score between 0-100 indicating regex performance",
    )
    false_negatives: List[str] = Field(
        ..., description="Valid inputs that were not matched"
    )
    false_positives: List[str] = Field(
        ..., description="Invalid inputs that were incorrectly matched"
    )
    feedback: str = Field(..., description="A human-readable explanation of the result")
    final_test_suite: dict[str, List[str]] = Field(
        ...,
        description="The final version of the test suite used for evaluation. It has 'valid' and 'invalid' keys.",
    )


# Define the regex problem (this can be customized)
regex_problem = "Match valid email addresses and reject invalid ones."

# Agent 1: Challenger
challenger = Agent(
    role="Regex Challenger",
    goal="Create rigorous test suites, evaluate regex solutions, and push for the best possible implementation",
    backstory=(
        "You are a master of edge-case detection in regex. You translate user problems into tests suites and relentlessly push implementers to make their regex bulletproof through waves of validation. Your test cases are legendary for covering scenarios that others miss."
    ),
    verbose=True,
)

# Agent 2: Regex Implementer
implementer = Agent(
    role="Regex Engineer",
    goal="Write the perfect regex pattern that passes all test cases with 100% accuracy",
    backstory=(
        "You're a seasoned regex builder with deep understanding of pattern matching. "
        "You study test suites carefully and respond with precise regex expressions to pass them all. "
        "Your patterns are elegant, efficient, and robust against edge cases."
    ),
    verbose=True,
)

# === TASKS ===

# Round 1: Generate initial test suite
generate_test_suite_round1 = Task(
    description=(
        f"""Based on this user problem: '{regex_problem}', generate a test cases.

        Create comprehensive test cases covering common patterns, edge cases, and tricky scenarios.
        The goal is to challenge the implementer but still create a fair and solvable problem.
        """
    ),
    expected_output="Test cases for regex problem",
    agent=challenger,
    output_pydantic=TestCasesOutput,
)


implement_regex_round1 = Task(
    description=(
        f"""Create the best possible regex pattern for this problem: '{regex_problem}'

        IMPORTANT: Return ONLY the regex pattern string itself, nothing else. No code, no explanation.
        """
    ),
    expected_output="A regex pattern string",
    agent=implementer,
    output_pydantic=RegexOutput,
    context=[generate_test_suite_round1],
)

# Round 1: Evaluate solution and create harder test suite
evaluate_and_challenge_round1 = Task(
    description=(
        """Evaluate the regex pattern submitted by the implementer.

        1. Use your execute_e2b tool to run the evaluation function with the submitted regex
        2. Analyze the results to identify any weaknesses
        3. Create a new, more challenging test suite that specifically targets these weaknesses
        4. Add at least 5-10 new edge cases that were not covered in the original test suite
        """
    ),
    expected_output="More challenging test suite",
    agent=challenger,
    tools=[execute_e2b],  # type: ignore
    output_pydantic=TestCasesOutput,
    context=[implement_regex_round1],
)

# Round 2: Implement improved regex solution
implement_regex_round2 = Task(
    description=(
        """Create an improved regex pattern that passes the enhanced test suite.

        The Challenger has identified weaknesses in your first solution and created more difficult test cases.
        Study these new cases carefully to understand what edge cases you need to handle.

        IMPORTANT: Return ONLY the regex pattern string itself, nothing else. No code, no explanation.
        """
    ),
    expected_output="An improved regex pattern string",
    agent=implementer,
    output_pydantic=RegexOutput,
    context=[evaluate_and_challenge_round1],
)

# Round 2: Create final, most challenging test suite
evaluate_and_challenge_round2 = Task(
    description=(
        """Evaluate the improved regex and create the FINAL challenge test suite.

        1. Evaluate the new regex against your enhanced test suite
        2. Identify any remaining weaknesses or edge cases
        3. Create the ultimate test suite with extremely challenging cases
        4. This should represent the hardest possible test for a regex solution to this problem

        Your final test suite should be comprehensive, covering all reasonable edge cases for this problem.
        """
    ),
    expected_output="Ultimate test cases",
    agent=challenger,
    context=[implement_regex_round2],
    tools=[execute_e2b],  # type: ignore
    output_pydantic=TestCasesOutput,
)

# Round 3: Implement final regex solution
implement_regex_final = Task(
    description=(
        """This is your FINAL opportunity to create the perfect regex pattern.

        The Challenger has created the ultimate test suite with extremely difficult edge cases.
        Your task is to create a regex pattern that handles ALL of these cases correctly.

        IMPORTANT: Return ONLY the regex pattern string itself, nothing else. No code, no explanation.
        """
    ),
    expected_output="The final, optimized regex pattern string",
    agent=implementer,
    output_pydantic=RegexOutput,
    context=[evaluate_and_challenge_round2],
)

# Final evaluation and presentation
final_evaluation = Task(
    description=(
        """Evaluate the final regex implementation and prepare the results for the user.

        1. Run the final regex against your ultimate test suite
        2. Calculate the final score and identify any remaining issues
        3. Prepare a comprehensive evaluation report including:
           - The final regex pattern
           - Score (percentage of tests passed)
           - Any false negatives and false positives
           - Detailed feedback on the quality of the solution
           - The complete test suite used for evaluation

        This report will be presented to the user as the final output of the challenge.
        """
    ),
    expected_output="Final evaluation report",
    agent=challenger,
    tools=[execute_e2b],  # type: ignore
    context=[implement_regex_final],
    output_pydantic=FinalEvaluationOutput,
)

# === CREW ===
regex_crew = Crew(
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
    process=Process.sequential,
    verbose=True,
)


# Function to run the crew with a specific regex problem
def run_regex_crew(problem=None):
    global regex_problem
    if problem:
        regex_problem = problem

        # Update task descriptions with the new regex problem
        generate_test_suite_round1.description = (
            generate_test_suite_round1.description.replace(
                "'{regex_problem}'", f"'{regex_problem}'"
            )
        )

        implement_regex_round1.description = implement_regex_round1.description.replace(
            "'{regex_problem}'", f"'{regex_problem}'"
        )

    print(f"🚀 Starting regex challenge for problem: '{regex_problem}'")
    result = regex_crew.kickoff()

    # Print the full result
    print("🏁 FINAL RESULT:", result)

    try:
        # Try to extract structured data from the result if available
        if isinstance(result, dict) and "final_regex" in result:
            # Direct dict access
            final_data = result
            print(f"Final Regex: {final_data.get('final_regex')}")
            print(f"Score: {final_data.get('score', 0)}/100")
            print(f"Feedback: {final_data.get('feedback', '')}")

            # Display false negatives if available
            false_negatives = final_data.get("false_negatives", [])
            if false_negatives:
                print(f"False Negatives ({len(false_negatives)}):")
                for item in false_negatives[:5]:  # Show at most 5 examples
                    print(f"  - {item}")
                if len(false_negatives) > 5:
                    print(f"  ... and {len(false_negatives) - 5} more")

            # Display false positives if available
            false_positives = final_data.get("false_positives", [])
            if false_positives:
                print(f"False Positives ({len(false_positives)}):")
                for item in false_positives[:5]:  # Show at most 5 examples
                    print(f"  - {item}")
                if len(false_positives) > 5:
                    print(f"  ... and {len(false_positives) - 5} more")
    except Exception as e:
        print(f"Note: Could not parse structured output: {e}")

    return result


if __name__ == "__main__":
    run_regex_crew()
