import re
import json


def test_regex(regex_pattern, test_cases):
    results = {"score": 0, "failures": []}

    total_cases = len(test_cases["valid"]) + len(test_cases["invalid"])
    passed_cases = 0

    # Compile regex (with error handling)
    try:
        pattern = re.compile(regex_pattern)
    except Exception as e:
        results["failures"].append(test_cases["valid"])
        results["failures"].append(test_cases["invalid"])
        results["score"] = 0
        return results

    # Test valid cases
    for valid in test_cases["valid"]:
        try:
            if pattern.fullmatch(valid):
                passed_cases += 1
            else:
                results["failures"].append(valid)
        except Exception as e:
            results["failures"].append(valid)

    for invalid in test_cases["invalid"]:
        try:
            if not pattern.fullmatch(invalid):
                passed_cases += 1
            else:
                results["failures"].append(invalid)
        except Exception as e:
            results["failures"].append(invalid)

    # Calculate score as percentage of passed cases
    if total_cases > 0:
        results["score"] = int((passed_cases / total_cases) * 100)

    return results
