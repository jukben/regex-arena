"""
Regex Crew - A CrewAI implementation for generating optimized regex patterns

This package uses CrewAI to create a collaborative system between a Challenger Agent
and a Regex Engineer Agent to produce the best possible regex for a given problem.
"""

from regex_crew.crew import run_regex_crew

# Define what's available when someone does "from regex_crew import *"
__all__ = ['run_regex_crew']
