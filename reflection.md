# PawPal+ Project Reflection

## 1. System Design

* A user should be able to enter and manage information about themselves and their pets
* A user should be able to add, edit, and manage pet care tasks with relevant details
* A user should be able to view a daily care plan based on available time and priorities

### a. Initial Design

* My initial UML design included four main classes: Owner, Pet, Task, and Scheduler
* The Owner class stores user information such as available time, preferences, and a list of pets
* The Pet class holds details about each pet, such as name, type, and age
* The Task class represents pet care activities, including duration, priority, and completion status
* The Scheduler class manages tasks and generates a daily plan based on constraints and priorities

### b. Design Changes

* Added a relationship between Task and Pet so each task is tied to a specific pet
* Connected Scheduler to Owner and removed duplicate available_time to ensure a single source of truth
* Linked Owner and Scheduler to integrate user data with scheduling logic
* Replaced update_task(info: dict) with explicit parameters for better safety and clarity
* Made helper methods (e.g., sorting and filtering) private to reflect internal logic
* Added missing methods such as remove_pet() and remove_task() to improve completeness
* Clarified the distinction between tasks (input) and generated_plan (output) in Scheduler

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and Priorities

* The scheduler considers available time, task priority, and basic task attributes (duration, category)
* Priority was treated as the most important factor, ensuring high-priority tasks are scheduled first
* Time constraints were enforced to ensure the total scheduled tasks fit within the owner's available time

### b. Tradeoffs

* I reviewed my conflict detection method using AI and received a more Pythonic version using defaultdict and list comprehensions

* I chose to keep my original version because it is more explicit and easier to understand

* The scheduler only detects conflicts when tasks have exactly the same scheduled time rather than overlapping durations

* This simplifies implementation and improves readability but may miss more complex conflicts

* This tradeoff prioritizes simplicity and clarity over full accuracy

---

## 3. AI Collaboration

### a. How I Used AI

* Used AI (Claude and Copilot) for design brainstorming and identifying core system components

* Generated class skeletons and method stubs based on UML design

* Assisted with implementing scheduling logic, sorting, filtering, and conflict detection

* Used AI for debugging by analyzing errors and failed tests

* Refined algorithms while maintaining control over readability and simplicity

* Most helpful prompts included:

  * Implementation requests (e.g., “implement this method based on my class structure”)
  * Debugging questions (e.g., “why is this test failing?”)
  * Design reviews (e.g., “are there missing relationships?”)
  * Context-aware prompts using specific files (e.g., `#file:pawpal_system.py`)

* Prompts with clear context and requirements produced the most accurate results

### b. Judgment and Verification

* I did not always accept AI suggestions directly, especially when they reduced readability
* For example, I rejected a more compact conflict detection implementation in favor of a clearer version
* I evaluated AI outputs by checking correctness, readability, and alignment with my system design

---

## 4. Testing and Verification

### a. What I Tested

* Verified sorting correctness to ensure tasks are ordered chronologically

* Tested recurring task logic to confirm daily tasks generate a new task with the correct next due date

* Checked conflict detection to ensure tasks scheduled at the same time are flagged

* Tested scheduling behavior to ensure tasks fit within available time constraints

* These tests were important because they validate core functionality and ensure algorithms behave correctly under normal and edge conditions

### b. Confidence

* I am confident (4/5) that the scheduler works correctly for core use cases

* The test suite confirms that sorting, filtering, recurrence, and conflict detection work as expected

* If I had more time, I would test:

  * Overlapping task durations (not just exact time conflicts)
  * Invalid or malformed time inputs (e.g., "abc", "25:99")
  * Behavior with a large number of tasks
  * Edge cases such as repeated task completion or pets with no tasks

---

## 5. Reflection

### a. What Went Well

* The system design remained consistent from UML to implementation
* Scheduling algorithms (sorting, filtering, recurrence, conflict detection) were successfully implemented
* AI tools accelerated development while allowing me to maintain control over decisions

### b. What I Would Improve

* Improve conflict detection to handle overlapping time ranges
* Enhance scheduling logic to be more optimized rather than purely greedy
* Improve the Streamlit UI for better usability and visual clarity

### c. Key Takeaway

* Designing systems requires balancing simplicity, readability, and functionality
* AI is most effective when used as a tool, with the developer acting as the lead architect
* Critical thinking and evaluation are essential when working with AI-generated solutions
