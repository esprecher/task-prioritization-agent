# Master debug flag for the entire script.
DEBUG = True

import json
from pprint import pformat

def log_debug(msg: str):
    """Print debug messages only when DEBUG is True."""
    if DEBUG:
        print(f"[DEBUG] {msg}")


# Create some sample tasks for testing purposes.
# Tasks are scored on a scale of 1-3 (1=low, 2=medium, 3=high) for each 
# of the following dimensions:
# - Importance: How important is this task to your goals?
# - Urgency: How soon does this task need to be done?
# - Desire: How much do you want to do this task?
# They also have a spot to add the estimate time to complete the task in minutes.
SAMPLE_TASKS = [
    {"title": "Email accountant", "importance": 3, "urgency": 3, "desire": 1, "est_minutes": 20},
    {"title": "Practice mandolin", "importance": 2, "urgency": 1, "desire": 3, "est_minutes": 30},
    {"title": "Go for a walk", "importance": 2, "urgency": 2, "desire": 2, "est_minutes": 20},
]

# Function for computing task priority score
#
# It is currently based on a weighted scoring that considers importance,
# urgency, and personal preference.  Urgency x Importance is a common
# way of thinking about task prioritization (note the Eisenhower Matrix).
# But desire to do something can take some ranking impact as well.
def compute_priority_score(task):
    """
    Compute a numeric priority score for a task.
    Transparent formula so we always know what's happening.
    Current formula upweights importance and urgency multiplicatively,
    but then adds "desire" to do the given task.
    """
    return (
        ((1.5 * task["importance"]) *
        (1 * task["urgency"])) +
        (1 * task["desire"])
    )


def score_tasks(tasks):
    """
    Add a `score` to each task and return them sorted by score (descending).
    """
    scored = []
    for t in tasks:
        t_copy = dict(t)
        t_copy["score"] = compute_priority_score(t_copy)
        scored.append(t_copy)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def choose_shortlist(scored_tasks, available_minutes=60):
    """
    Choose a shortlist of tasks that fit within the given time budget.
    Full debug prints an explaination of each decision.
    """
    remaining = available_minutes
    shortlist = []

    log_debug(f"Starting shortlist selection with {available_minutes} minutes.")
    for t in scored_tasks:
        title = t['title']
        est = t['est_minutes']
        score = t['score']

        log_debug(f"Considering: {title} (score={score}, est={est} min)")
        
        if est <= remaining:
            shortlist.append(t)
            remaining -= est
            log_debug(f"-> SELECTED. {remaining} minutes remaining.")
        else:
            log_debug(f"-> SKIPPED (not enough time). Still {remaining} minutes left.")

    log_debug(f"Selection complete. Final remaining minutes: {remaining}.")
    return shortlist


def assemble_plan_data(shortlist, all_tasks, available_minutes, energy_level):
    """
    Assemble a clean JSON-friendly dictionary representing
    the user's constraints and the system's deterministic choices.
    """
    data = {
        "available_minutes": available_minutes,
        "energy_level": energy_level,
        "shortlist": shortlist,
        "all_tasks": all_tasks,
    }
    log_debug(f"Constructed plan data with {len(shortlist)} shortlist tasks.")
    return data

# Main function
if __name__ == "__main__":
    print("=== Raw Tasks ===")
    for t in SAMPLE_TASKS:
        print("-", t["title"])

    scored = score_tasks(SAMPLE_TASKS)

    print("\n=== Scored & Sorted Tasks (debug) ===")
    for t in scored:
        print(
            f"{t['score']:>4} - {t['title']} | "
            f"imp={t['importance']} urg={t['urgency']} "
            f"des={t['desire']} drag={t.get('drag', 'NA')} "
            f"est={t['est_minutes']} min"
        )
    
    print("\n=== Shortlist (deterministic, debug) ===")
    shortlist = choose_shortlist(scored, available_minutes=60)

    for t in shortlist:
        print(f"- {t['title']} ({t['est_minutes']} min, score={t['score']})")
    
    log_debug(f"Final shortlist: {[t['title'] for t in shortlist]}")

    print("\n=== Assembling Plan Data (debug) ===")
    plan_data = assemble_plan_data(
        shortlist=shortlist,
        all_tasks=scored,
        available_minutes=60,
        energy_level="medium",
    )
    log_debug("Plan data contents:\n" + pformat(plan_data, indent=2))