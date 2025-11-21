"""
Plan Explainer Agent

Uses the existing deterministic planning logic (score_tasks, choose_shortlist,
assemble_plan_data) and asks Gemini to explain the plan to the user.
"""

import json
import re
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
        "1) Explain why this shortlist is a good plan,\n"
        "2) Optionally adjust the shortlist slightly if it would clearly improve it,\n"
        "3) Suggest 0–2 'nice to have' tasks if there is extra time or energy.\n\n"
        "IMPORTANT:\n"
        "- You MUST respond with a single valid JSON object only.\n"
        "- Do NOT include any text before or after the JSON.\n"
        "- Do NOT wrap the JSON in Markdown code fences (no ```json ... ```).\n"
        "- The JSON must have exactly these fields:\n"
        "  - 'shortlist': list of {title, reason, est_minutes, score}\n"
        "  - 'nice_to_have': list of {title, reason, est_minutes, score}\n"
        "  - 'summary': a short string explaining the overall plan.\n"
    )

    user_prompt = (
        "Here is the current plan data as JSON.\n"
        "Use it to construct your JSON response as described in the system instructions.\n\n"
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
    
    print("\n\n-----\n[Parsed JSON Plan]")
    raw_text = response.text.strip()

    # If the model wrapped the JSON in Markdown code fences, strip them.
    if raw_text.startswith("```"):
        # Remove leading ``` or ```json line
        first_newline = raw_text.find("\n")
        if first_newline != -1:
            raw_text = raw_text[first_newline + 1 :]
        # Remove trailing ```
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()

    try:
        plan_json = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print("ERROR: Failed to parse JSON from model response:", e)
        print("Raw text was:\n", raw_text)
        return

    # Pretty-print the parsed structure
    print(json.dumps(plan_json, indent=2))

    # Optionally: show shortlist titles
    print("\nShortlist tasks chosen by the agent:")
    for t in plan_json.get("shortlist", []):
        print(f"- {t.get('title')} (est={t.get('est_minutes')} min, score={t.get('score')})")
    
    
    # Better human-readable output
    print("\n\n=== Final Task Plan ===")

    # Shortlist section
    print("\nShortlist (focus tasks):")
    for t in plan_json.get("shortlist", []):
        title = t.get("title")
        est = t.get("est_minutes")
        score = t.get("score")
        reason = t.get("reason")
        print(f"- {title} [{est} min, score={score}]")
        print(f"  Reason: {reason}")

    # Nice-to-have section
    nice_to_have = plan_json.get("nice_to_have", [])
    if nice_to_have:
        print("\nNice-to-have tasks (optional):")
        for t in nice_to_have:
            title = t.get("title")
            est = t.get("est_minutes")
            score = t.get("score")
            reason = t.get("reason")
            print(f"- {title} [{est} min, score={score}]")
            print(f"  Reason: {reason}")
    else:
        print("\nNo nice-to-have tasks suggested for this session.")

    # Summary
    summary = plan_json.get("summary")
    if summary:
        print("\nSummary:")
        print(summary)


if __name__ == "__main__":
    main()