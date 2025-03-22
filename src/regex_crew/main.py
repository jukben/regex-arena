#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from regex_crew.crew import run_regex_crew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "regex_problem": "Match valid email addresses and reject invalid ones."
    }
    
    try:
        run_regex_crew()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

