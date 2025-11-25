"""
ADK root agent for the Task Prioritization Advisor.

This agent exposes a single tool that runs the full Python pipeline:
- Parse tasks (via ParseTasksAgent)
- Score and shortlist deterministically
- Let the Planning Agent decide the final shortlist and nice-to-have tasks
- Return the final plan JSON
"""

import os
import sys

# Ensure the project root is on sys.path so that `src` can be imported
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import Dict, Any

from google.adk.agents import Agent

# Import your existing Python-level orchestrator
from src.task_advisor import run_task_advisor


def log_debug(msg: str) -> None:
    """Lightweight debug logger for the root agent."""
    print(f"==== [root_agent] {msg}")


def run_task_advisor_tool(
    raw_tasks_str: str,
    available_minutes: int = 60,
    energy_level: str = "medium",
) -> Dict[str, Any]:
    """
    Tool wrapper that runs the full task advisor pipeline.

    Args:
        raw_tasks_str: Task list provided by the user (JSON-like text).
        available_minutes: Time budget for this session.
        energy_level: User's current energy level ("low", "medium", "high").

    Returns:
        The final plan JSON as a Python dict, including:
        - shortlist
        - nice_to_have
        - summary
    """
    log_debug(
        f"Calling run_task_advisor with available_minutes={available_minutes}, "
        f"energy_level={energy_level}"
    )
    plan_json = run_task_advisor(
        tasks=None,
        raw_tasks_str=raw_tasks_str,
        available_minutes=available_minutes,
        energy_level=energy_level,
    )
    log_debug("Received plan_json from run_task_advisor.")
    return plan_json


root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="task_advisor_root",
    description="Helps users turn a messy task list into a prioritized short plan.",
    instruction=(
        "You are a Personal Task Prioritization Advisor.\n"
        "Your job is to help the user turn their tasks into a focused, "
        "realistic short plan for the next block of time.\n\n"
        "Workflow:\n"
        "1) Ask the user to paste or describe their task list. "
        "   If they can provide valid JSON or nearly-valid JSON, that's ideal.\n"
        "2) Ask how many minutes they have and what their current energy level is.\n"
        "3) Use the 'run_task_advisor_tool' to generate a structured plan.\n"
        "4) Explain the plan to the user in friendly language, and invite tweaks.\n\n"
        "IMPORTANT:\n"
        "- Always use the tool for actual planning.\n"
        "- You can chat normally for clarifying questions and follow-ups.\n"
    ),
    tools=[run_task_advisor_tool],
)