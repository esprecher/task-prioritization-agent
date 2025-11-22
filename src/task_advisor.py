"""
Task Advisor Root Orchestrator

This module provides a single entrypoint:
    run_task_advisor(tasks=None, raw_tasks_str=None,
                      available_minutes=60, energy_level="medium")

Right now:
- tasks defaults to SAMPLE_TASKS
- raw_tasks_str is reserved for Phase 1 Step 3 (parse-tasks agent)

This file will become the root orchestrator for the ADK agent system.
"""

from dotenv import load_dotenv
import os

from main import SAMPLE_TASKS, score_tasks, choose_shortlist, assemble_plan_data
from plan_explainer_agent import call_planning_agent, print_final_plan


def run_task_advisor(
    tasks=None,
    raw_tasks_str=None,
    available_minutes=60,
    energy_level="medium"
):
    """
    Root orchestrator for the Task Advisor (Python-level).
    This will later be replaced or wrapped by the ADK root agent.

    Parameters:
        tasks: list of task dicts (optional)
        raw_tasks_str: string containing raw task input (reserved for Step 3)
        available_minutes: int
        energy_level: str
    """

    # Phase 1: If no tasks provided, use SAMPLE_TASKS
    if tasks is None:
        tasks = SAMPLE_TASKS

    # ---- Step A: Score tasks (deterministic) ----
    scored = score_tasks(tasks)

    # ---- Step B: Choose shortlist (deterministic, for now) ----
    shortlist = choose_shortlist(scored, available_minutes=available_minutes)

    # ---- Step C: Build plan_data ----
    plan_data = assemble_plan_data(
        shortlist=shortlist,
        all_tasks=scored,
        available_minutes=available_minutes,
        energy_level=energy_level,
    )

    # ---- Step D: Call the planning agent ----
    plan_json = call_planning_agent(plan_data)

    # ---- Step E: Pretty-print output ----
    print_final_plan(plan_json)

    return plan_json


def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    print("API Key Loaded:", bool(api_key))

    # Demo scenario
    run_task_advisor(
        tasks=SAMPLE_TASKS,
        available_minutes=60,
        energy_level="medium"
    )


if __name__ == "__main__":
    main()