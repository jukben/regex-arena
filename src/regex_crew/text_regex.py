import re
import json

def test_regex(regex_pattern, test_cases):
    results = {
        "passed": True,
        "score": 0,
        "false_negatives": [],
        "false_positives": [],
        "failures": []
    }
    
    total_cases = len(test_cases["valid"]) + len(test_cases["invalid"])
    passed_cases = 0
    
    # Compile regex (with error handling)
    try:
        pattern = re.compile(regex_pattern)
    except Exception as e:
        results["passed"] = False
        results["failures"].append(f"Error compiling regex: {str(e)}")
        results["score"] = 0
        return results
    
    # Test valid cases
    for valid in test_cases["valid"]:
        try:
            if pattern.fullmatch(valid):
                passed_cases += 1
            else:
                results["passed"] = False
                results["failures"].append(f"Failed to match valid input: {valid}")
                results["false_negatives"].append(valid)
        except Exception as e:
            results["passed"] = False
            results["failures"].append(f"Error with regex on valid input {valid}: {str(e)}")
            results["false_negatives"].append(valid)
    
    # Test invalid cases
    for invalid in test_cases["invalid"]:
        try:
            if not pattern.fullmatch(invalid):
                passed_cases += 1
            else:
                results["passed"] = False
                results["failures"].append(f"Incorrectly matched invalid input: {invalid}")
                results["false_positives"].append(invalid)
        except Exception as e:
            results["passed"] = False
            results["failures"].append(f"Error with regex on invalid input {invalid}: {str(e)}")
            # This is technically not a false positive but we categorize it as such
            # since the regex should handle all inputs without errors
            results["false_positives"].append(invalid)
    
    # Calculate score as percentage of passed cases
    if total_cases > 0:
        results["score"] = int((passed_cases / total_cases) * 100)
    
    return results

# Setup test cases
test_cases = {
    "valid": ['test@example.com'],
    "invalid": ['invalid-email']
}

# Run test and print results
try:
    results = test_regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", test_cases)
    print(json.dumps(results, indent=2))
except Exception as e:
    print(json.dumps({"error": str(e), "passed": False, "score": 0}, indent=2))