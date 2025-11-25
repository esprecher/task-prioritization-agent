# Task Advisor Agent

*A Lightweight, Agentic Personal Task Prioritization Assistant*

---

## Overview
The **Task Advisor Agent** is a lightweight, agentic system that helps users decide *what to work on next* based on available time, energy, and a list of pending tasks. It combines:

- **Deterministic logic** (for scoring and shortlist generation)
- **LLM-based agentic reasoning** (for explaining, refining, and improving the plan)
- **The Google Agent Development Kit (ADK)** (for orchestration and interactive CLI use)

Users can input tasks in flexible formats (JSON, partial fields, or mixed structure), and the system normalizes them, computes scores, selects a shortlist, and then uses an LLM-based agent to generate a final, human-friendly plan.

This project was developed as the **Capstone** for the *Kaggle + Google 5‑Day Intensive: Generative AI Agentic Program*.

---

## Features
- **Natural-language task intake** through a Parse Tasks Agent
- **Deterministic scoring + shortlist selection** based on time and energy
- **AI planning agent** to refine or adjust the shortlist
- **Root agent (ADK)** orchestrating the entire workflow
- **Clear, readable CLI output** with optional debug logs
- **Modular architecture** designed for iterative improvements

---

## Repository Structure
```
project-root/
├── agents/
│   └── task_advisor_agent/
│       ├── agent.py                 # Root ADK agent
│       └── __init__.py
├── src/
│   ├── main.py                      # Deterministic scoring + shortlist logic
│   ├── parse_tasks_agent.py         # LLM-based task normalizer
│   ├── plan_explainer_agent.py      # LLM-based planning/explanation
│   └── task_advisor.py              # Combined pipeline (initial Python version)
├── .env                             # Contains GOOGLE_API_KEY
└── README.md                        # This file
```

---

## Installation & Setup
### **1. Clone the repository**
```
git clone https://github.com/esprecher/task-prioritization-agent
cd task-prioritization-agent
```

### **2. Install dependencies**
```
pip install -r requirements.txt
```

### **3. Set the environment variable**
Create a `.env` file:
```
GOOGLE_API_KEY=your-key-here
```

### **4. Run the ADK agent**
From project root:
```
adk run agents/task_advisor_agent
```

You will enter an interactive CLI where you can talk directly with your agent.

---

## Usage Example
**User:**
```
I’ve got 45 minutes and low energy. Tasks:
- email landlord (importance 3, urgency 2)
- stretch (desire 3)
- clean kitchen (urgency 3)
```

**Agent Output (abridged):**
```
Shortlist:
1. email landlord — quick high‑priority task
2. clean kitchen — fits remaining time well

Nice‑to‑have:
- stretch — good low‑energy choice

Summary:
Focus on emailing the landlord and cleaning the kitchen. Stretch if time/energy allow.
```

---

## Architecture Overview
The system follows a **hybrid pipeline**:

### **1. Parse Tasks Agent (LLM)**
Normalizes raw, messy, or incomplete input into:
```
[{title, importance, urgency, desire, est_minutes}, ...]
```
Missing fields are imputed.

### **2. Deterministic Planner**
- Scores tasks
- Selects shortlist based on available minutes
- Builds a structured `plan_data` payload

### **3. Planning Agent (LLM)**
Given `plan_data`, the model:
- Chooses the final shortlist
- Optionally adds 0–2 “nice to have” tasks
- Generates natural‑language reasoning

### **4. ADK Root Agent**
Coordinates the entire process:
- Parses user messages
- Calls ParseTasksAgent
- Runs deterministic planners
- Calls PlanningAgent
- Returns clean, user‑friendly output

---

## Future Improvements
If more time were available, next steps would focus on **deeper agentic reasoning** and **more adaptive collaboration**:

- **More flexible natural‑language task intake** (paragraphs, mixed formats, messy text)
- **Persistent agent memory** (user energy patterns, preferences, task tendencies)
- **Conversational task refinement**, including:
  - breaking large projects into subtasks
  - identifying bottlenecks or dependencies
  - applying the 80/20 rule
  - aligning tasks with personal goals
- **Agentic self‑critique & adjustment** to improve consistency
- **More dynamic reasoning** about time, attention, and cognitive load

These improvements would deepen the system’s value without requiring heavy UI, calendar APIs, or external task manager integrations.

---

## Acknowledgments
This project was developed for the **Kaggle + Google 5‑Day Generative AI Intensive (Agentic AI Capstone)**.

Special thanks to:
- **Kaggle** and **Google** for creating and hosting the course
- **ChatGPT** and **Google Gemini** — both of which were used collaboratively for architecture design, debugging, and development support throughout this project

Their combined assistance accelerated the building of a robust, agentic system within a short timeframe.

