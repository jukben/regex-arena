
from crewai.tools import tool
from e2b_code_interpreter import Sandbox
from typing import List 
from pydantic import BaseModel, Field



class TestSuite(BaseModel):
    valid: List[str] = Field(..., description="A list of valid email address strings")
    invalid: List[str] = Field(..., description="A list of invalid email address strings")

class TestCasesOutput(BaseModel):
    test_cases: TestSuite = Field(..., description="Dictionary with 'valid' and 'invalid' test cases")

@tool("E2B Sandbox")  
def execute_e2b(regex: str, test_cases: TestSuite) -> str | None:
    """
    Execute Python code and return the results.
    """
    with Sandbox() as sandbox:
        execution = sandbox.run_code(generate_test_sandbox_for_regex(regex, test_cases))
        return execution.text
    
def generate_test_sandbox_for_regex(regex: str, test_cases: TestSuite) -> str:
    return f"""
    import re
    import json

    def test_regex(regex, test_cases):
        results = {{"passed": True, "failures": [], "score": 0, "false_positives": [], "false_negatives": []}}
        
        total_cases = len(test_cases['valid']) + len(test_cases['invalid'])
        passed_cases = 0
        
        # Test valid cases
        for valid in test_cases['valid']:
            try:
                if re.fullmatch(regex, valid):
                    passed_cases += 1
                else:
                    results["passed"] = False
                    results["failures"].append(f"Failed to match valid input: {{valid}}")
                    results["false_negatives"].append(valid)
            except Exception as e:
                results["passed"] = False
                results["failures"].append(f"Error with regex on valid input {{valid}}: {{str(e)}}")
                results["false_negatives"].append(valid)
        
        # Test invalid cases
        for invalid in test_cases['invalid']:
            try:
                if not re.fullmatch(regex, invalid):
                    passed_cases += 1
                else:
                    results["passed"] = False
                    results["failures"].append(f"Incorrectly matched invalid input: {{invalid}}")
                    results["false_positives"].append(invalid)
            except Exception as e:
                results["passed"] = False
                results["failures"].append(f"Error with regex on invalid input {{invalid}}: {{str(e)}}")
                results["false_positives"].append(invalid)
        
        # Calculate score as percentage of passed cases
        if total_cases > 0:
            results["score"] = int((passed_cases / total_cases) * 100)
        
        return results

    try:
        results = test_regex('{regex}', {test_cases})
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({{"passed": False, "error": str(e), "score": 0}}, indent=2)
    """