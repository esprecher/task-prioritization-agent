
# Create some sample tasks for testing purposes
SAMPLE_TASKS = [
    {"title": "Email accountant", "importance": 3, "urgency": 3, "desire": 1, "drag": 3, "est_minutes": 20},
    {"title": "Practice mandolin", "importance": 2, "urgency": 1, "desire": 3, "drag": 1, "est_minutes": 30},
    {"title": "Go for a walk", "importance": 2, "urgency": 2, "desire": 2, "drag": 1, "est_minutes": 20},
]


# Main function
if __name__ == "__main__":
    print("=== Raw Tasks ===")
    for t in SAMPLE_TASKS:
        print("-", t["title"])