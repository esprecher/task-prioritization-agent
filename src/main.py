
# Create some sample tasks for testing purposes.
# Tasks are scored on a scale of 1-3 (1=low, 2=medium, 3=high) for each 
# of the following dimensions:
# - Importance: How important is this task to your goals?
# - Urgency: How soon does this task need to be done?
# - Desire: How much do you want to do this task?
# They also have a spot to add the estimate time to complete the task in minutes.
SAMPLE_TASKS = [
    {"title": "Email accountant", "importance": 3, "urgency": 3, "desire": 1, "drag": 3, "est_minutes": 20},
    {"title": "Practice mandolin", "importance": 2, "urgency": 1, "desire": 3, "drag": 1, "est_minutes": 30},
    {"title": "Go for a walk", "importance": 2, "urgency": 2, "desire": 2, "drag": 1, "est_minutes": 20},
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


# Main function
if __name__ == "__main__":
    print("\n=== Scored Tasks (debug) ===")
    for t in SAMPLE_TASKS:
        score = compute_priority_score(t)
        print(
            f"{score:>2} - {t['title']} | "
            f"imp={t['importance']} urg={t['urgency']} "
            f"des={t['desire']} drag={t['drag']}"
        )
