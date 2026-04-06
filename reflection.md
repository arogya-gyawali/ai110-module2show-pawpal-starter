# PawPal+ Project Reflection

## 1. System Design

- user should be able to enter and manage information about their pet and themselves
- add edit and manage pet care tasks, include the details of the task here
- user should be able to view a daily care plan, based on their available time etc.

**a. Initial design**

- Briefly describe your initial UML design.
- Initial design has 4 classes, Owner, Pet, Task, and Schedular.

- What classes did you include, and what responsibilities did you assign to each?
- The Owner class represents the user of the system and is responsible for storing information such as available time, preferences, and a list of pets. The Pet class holds details about each pet, including attributes like name, type, and age. The Task class represents individual pet care activities, such as feeding or walking, and includes information like duration, priority, and completion status. The Scheduler class is responsible for managing tasks and generating a daily plan based on the owner's available time and task priorities.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.


* Added a relationship between Task and Pet by including a pet attribute in the Task class so each task is tied to a specific pet.

* Connected Scheduler to Owner and removed available_time from Scheduler to avoid duplication and ensure a single source of truth.

* Added a link between Owner and Scheduler so user data, pets, and scheduling logic are properly connected.

* Replaced update_task(info: dict) with explicit parameters to make the method safer and clearer.

* Made helper methods like sorting and filtering private (e.g., _sort_tasks_by_priority) to better reflect that they are internal logic.

* Added missing methods such as remove_pet() in Owner and remove_task() in Scheduler to make the system more complete.

* Clarified the distinction between tasks (input list) and generated_plan (final scheduled output) in the Scheduler.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- 2b. Tradeoffs:

I reviewed my conflict detection method using AI and received a more Pythonic version that used defaultdict and a list comprehension to make the code more concise. While this version is shorter and slightly more efficient, I chose to keep my original implementation because it is more explicit and easier to understand.

Additionally, my scheduler only detects conflicts when tasks have exactly the same scheduled time rather than checking for overlapping durations. This simplifies the implementation but may miss more complex scheduling conflicts. This tradeoff prioritizes readability and simplicity over full accuracy.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
