"""
Plan Explainer Agent

Uses the existing deterministic planning logic (score_tasks, choose_shortlist,
assemble_plan_data) and asks Gemini to explain the plan to the user.
"""

import json
from pprint import pformat

from dotenv import load_dotenv
import os
from google import genai

# Import your existing logic
from main import SAMPLE_TASKS, score_tasks, choose_shortlist, assemble_plan_data, log_debug, DEBUG


MODEL_NAME = "gemini-2.5-flash-lite"


def build_demo_plan_data():
    """
    Reuse the deterministic pipeline to create plan_data
    that we can hand to the model.
    """
    scored = score_tasks(SAMPLE_TASKS)
    shortlist = choose_shortlist(scored, available_minutes=60)
    plan_data = assemble_plan_data(
        shortlist=shortlist,
        all_tasks=scored,
        available_minutes=60,
        energy_level="medium",
    )
    log_debug("Plan data assembled in plan_explainer_agent:\n" + pformat(plan_data, indent=2))
    return plan_data


def main():
    # 1. Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    print("API Key Loaded:", bool(api_key))

    # 2. Build deterministic plan_data
    plan_data = build_demo_plan_data()

    # 3. Initialize client
    client = genai.Client()

    # 4. Prepare prompts
    system_instruction = (
        "You are a Personal Task Prioritization Advisor.\n"
        "You receive a JSON object describing:\n"
        "- all tasks with scores and attributes\n"
        "- a shortlist of tasks chosen by a deterministic planner\n"
        "- the user's available time and energy level\n\n"
        "Your job is to:\n"
        "1) Explain in clear, friendly language why this shortlist is a good plan,\n"
        "2) Mention any tradeoffs that were made,\n"
        "3) Optionally suggest one small tweak if it would clearly help.\n"
    )

    user_prompt = (
        "Here is the current plan data as JSON.\n"
        "Please analyze it and then explain the plan to the user.\n\n"
        "PLAN_DATA_JSON:\n"
        + json.dumps(plan_data, indent=2)
    )

    print("\n[User → Model]")
    print(user_prompt)

    # 5. Call the model
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            {"role": "user", "parts": [{"text": system_instruction + "\n\n" + user_prompt}]}
        ],
    )

    print("\n[Model Explanation]")
    print(response.text)


if __name__ == "__main__":
    main()