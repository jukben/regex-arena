"""
Regex Crew Runner

This script provides a simple way to run the Regex Crew with different regex problems.
"""
import sys
import os
from dotenv import load_dotenv
from regex_crew.crew import run_regex_crew

# Load environment variables
load_dotenv()

def main():
    """Run the Regex Crew with a specified problem or default"""
    # Check if API keys are set
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ Error: GEMINI_API_KEY environment variable is not set!")
        print("Please check your .env file or set it manually.")
        sys.exit(1)
    
    if not os.getenv("E2B_API_KEY"):
        print("⚠️ Error: E2B_API_KEY environment variable is not set!")
        print("Please check your .env file or set it manually.")
        sys.exit(1)

    # Set Google API environment variable from GEMINI_API_KEY
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")
    
    # Get the regex problem from command line arguments if provided
    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
        run_regex_crew(problem)
    else:
        # Run with the default problem
        run_regex_crew()

if __name__ == "__main__":
    main() 