
from crewai.tools import tool
from e2b_code_interpreter import Sandbox


@tool("Python Interpreter")  
def execute_python(code: str) -> str | None:
    """
    Execute Python code and return the results.
    """
    with Sandbox() as sandbox:
        execution = sandbox.run_code(code)
        return execution.text
