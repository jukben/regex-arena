"""
Custom callbacks for CrewAI to track agent activities.

These callbacks log all agent interactions, task executions, and results
to both the console and a log file.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# Configure logging
def setup_logging(log_dir="logs"):
    """Set up logging to both console and file."""
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)

    # Create a unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"regex_crew_{timestamp}.log")

    # Configure root logger
    logger = logging.getLogger("regex_crew")
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Create console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s | %(message)s")
    console.setFormatter(console_format)

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger


# Create logger
logger = setup_logging()


# Universal callback handler that works with any CrewAI version
class RegexCallbackHandler:
    """Unified callback handler for all CrewAI events."""

    def on_agent_start(self, agent) -> Any:
        """Called when an agent starts working."""
        logger.info(f"🤖 Agent '{agent.role}' started working")

    def on_agent_finish(self, agent, output) -> Any:
        """Called when an agent finishes its work."""
        logger.info(f"✅ Agent '{agent.role}' finished")
        logger.debug(
            f"Output from '{agent.role}':\n{output[:100]}..."
            if len(output) > 100
            else output
        )

    def on_tool_start(self, agent, tool_name, input_str) -> Any:
        """Called when an agent starts using a tool."""
        logger.info(f"🔧 Agent '{agent.role}' started using tool '{tool_name}'")
        logger.debug(
            f"Tool input: {input_str[:100]}..." if len(input_str) > 100 else input_str
        )

    def on_tool_finish(self, agent, tool_name, output) -> Any:
        """Called when an agent finishes using a tool."""
        logger.info(f"🔧 Agent '{agent.role}' finished using tool '{tool_name}'")
        logger.debug(f"Tool output: {output[:100]}..." if len(output) > 100 else output)

    def on_task_start(self, task) -> Any:
        """Called when a task starts."""
        task_desc = str(task)
        if hasattr(task, "description"):
            task_desc = task.description.splitlines()[0][:50] + "..."
        logger.info(f"📋 Task started: {task_desc}")

    def on_task_finish(self, task, output) -> Any:
        """Called when a task finishes."""
        task_desc = str(task)
        if hasattr(task, "description"):
            task_desc = task.description.splitlines()[0][:50] + "..."
        logger.info(f"✅ Task finished: {task_desc}")
        logger.debug(f"Task output: {output[:100]}..." if len(output) > 100 else output)

    def on_crew_start(self, crew) -> Any:
        """Called when a crew starts working."""
        logger.info(f"🚀 Crew started")
        if hasattr(crew, "tasks") and crew.tasks:
            try:
                task_descriptions = [
                    f"- {t.description.splitlines()[0][:50]}..." for t in crew.tasks
                ]
                logger.debug(f"Tasks in the crew:\n" + "\n".join(task_descriptions))
            except:
                pass

    def on_crew_finish(self, crew, output) -> Any:
        """Called when a crew finishes its work."""
        logger.info("🏁 Crew finished execution")

        # Try to pretty-print the output if it's a dict
        if isinstance(output, dict):
            try:
                output_str = json.dumps(output, indent=2)
                logger.debug(f"Crew output:\n{output_str}")
            except:
                logger.debug(f"Crew output: {str(output)}")
        else:
            logger.debug(f"Crew output: {str(output)}")

    def on_agent_error(self, agent, error) -> Any:
        """Called when an agent encounters an error."""
        logger.error(f"❌ Agent '{agent.role}' encountered an error: {str(error)}")

    def on_task_error(self, task, error) -> Any:
        """Called when a task encounters an error."""
        task_desc = str(task)
        if hasattr(task, "description"):
            task_desc = task.description.splitlines()[0][:50] + "..."
        logger.error(f"❌ Task '{task_desc}' encountered an error: {str(error)}")

    def on_crew_error(self, crew, error) -> Any:
        """Called when a crew encounters an error."""
        logger.error(f"❌ Crew encountered an error: {str(error)}")


# Create unified callback handler
def get_regex_crew_callbacks():
    """Return a list of callback handlers for the regex crew."""
    return [RegexCallbackHandler()]
