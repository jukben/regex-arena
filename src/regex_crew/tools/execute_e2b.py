from crewai.tools import tool
from e2b_code_interpreter import Sandbox
from typing import List
from pydantic import BaseModel, Field
import json


class TestSuite(BaseModel):
    valid: List[str] = Field(..., description="A list of valid strings")
    invalid: List[str] = Field(..., description="A list of invalid strings")


class TestCasesOutput(BaseModel):
    test_cases: TestSuite = Field(
        ..., description="Dictionary with 'valid' and 'invalid' test cases"
    )


@tool("Execute regex testing in sandbox")
def execute_e2b(regex: str, test_cases: TestSuite) -> str:
    """
    Execute Python code in a sandbox to test regex against test cases.

    Args:
        regex: The regex pattern to test
        test_cases: A TestSuite object with valid and invalid test cases

    Returns:
        String with evaluation results
    """

    print("Regex input", regex, "test_cases", test_cases)
    try:
        with Sandbox() as sandbox:
            code = generate_test_sandbox_for_regex(regex, test_cases)
            execution = sandbox.run_code(code)
            print("Execution", execution.logs)
            return execution.logs
    except Exception as e:
        return f"Error executing code in sandbox: {str(e)}"


def generate_test_sandbox_for_regex(regex: str, test_cases: TestSuite) -> str:
    """Generate Python code to test a regex pattern against test cases."""

    # Read the template file
    with open("src/regex_crew/tools/regex_evaluate_template.py", "r") as f:
        template = f.read()

    # Add the test execution code at the end
    return f"""
{template}

test_cases = {{
    "valid": {test_cases.valid},
    "invalid": {test_cases.invalid}
}}

regex = "{regex}"
res = test_regex(regex, test_cases)
print(json.dumps(res, indent=2))
"""
