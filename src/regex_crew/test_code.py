from regex_crew.tools.regex_evaluate_template import test_regex

test_cases = {"valid": ["test@example.com", "invalid-email"], "invalid": []}
regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

regex_eval = test_regex(regex, test_cases)

print(regex_eval)
