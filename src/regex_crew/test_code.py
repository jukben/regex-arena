



from regex_crew.text_regex import test_regex
from regex_crew.tools.execute_e2b import generate_test_sandbox_for_regex



test_cases = {"valid": ["test@example.com", "invalid-email"], "invalid": []}
regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


code = generate_test_sandbox_for_regex(regex, test_cases) # type: ignore


#print(dic)
#print(code)


regex_eval = test_regex(regex, test_cases)
print(regex_eval)