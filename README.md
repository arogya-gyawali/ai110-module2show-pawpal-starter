# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ now includes several improvements that make the scheduling system more intelligent and practical for real-world use:

* **Sorting by Time**: Tasks can be ordered by their scheduled time (HH:MM), helping create a clear daily timeline.
* **Filtering Options**: Tasks can be filtered by pet name or completion status, making it easier to manage and view relevant tasks.
* **Recurring Tasks**: Tasks marked as daily or weekly are automatically regenerated after completion using updated due dates.
* **Conflict Detection**: The system identifies tasks scheduled at the same time and provides warning messages instead of failing.

These features enhance usability by making the system more organized, responsive, and closer to real-life pet care planning.


## Testing PawPal+

You can run the automated test suite using:

```
python -m pytest
```

The tests verify key behaviors of the system, including:

* Sorting tasks by scheduled time
* Recurring task generation (daily tasks create new tasks)
* Conflict detection for tasks scheduled at the same time

These tests include both normal scenarios and edge cases to ensure the system behaves correctly.

### Confidence Level

⭐⭐⭐⭐☆ (4/5)

The system performs reliably for core features such as scheduling, filtering, recurrence, and conflict detection. While some logic is simplified (e.g., conflict detection only checks exact time matches), the test suite confirms that the main functionality works as expected.
