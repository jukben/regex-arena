import re
import json


def test_regex(regex: str, test_cases: dict) -> dict:
    """
    Test a regex pattern against provided test cases.

    Args:
        regex: Regular expression pattern to test
        test_cases: Dictionary with 'valid' and 'invalid' test cases

    Returns:
        Dictionary with test results
    """
    pattern = re.compile(regex)
    results = {
        "valid_matches": [],
        "valid_non_matches": [],
        "invalid_matches": [],
        "invalid_non_matches": [],
    }

    for test in test_cases.get("valid", []):
        if pattern.match(test):
            results["valid_matches"].append(test)
        else:
            results["valid_non_matches"].append(test)

    for test in test_cases.get("invalid", []):
        if pattern.match(test):
            results["invalid_matches"].append(test)
        else:
            results["invalid_non_matches"].append(test)

    return results
