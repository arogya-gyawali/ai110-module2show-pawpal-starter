from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from datetime import date, timedelta


@dataclass
class Pet:
    """Represents a pet owned by an Owner, along with its associated care tasks."""

    name: str
    type: str
    age: int
    special_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def update_info(self, info: dict) -> None:
        """Update pet attributes using a dictionary of field names and new values."""
        for key, value in info.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet and link the task back to this pet."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Task:
    """Represents a single care task assigned to a pet with a priority and duration."""

    name: str
    duration: int       # in minutes
    priority: int
    category: str
    pet: Optional[Pet] = None           # the pet this task belongs to
    completed: bool = False
    time: Optional[str] = None          # scheduled start time in "HH:MM" format
    frequency: str = "once"             # recurrence: "once", "daily", or "weekly"
    due_date: Optional[date] = None     # when this task is due

    def update_task(
        self,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
        category: Optional[str] = None,
    ) -> None:
        """Update one or more task fields, leaving unspecified fields unchanged."""
        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if category is not None:
            self.category = category

    def mark_complete(self) -> Optional[Task]:
        """Mark this task as completed. For recurring tasks, returns a new Task
        with the next due_date; otherwise returns None."""
        self.completed = True

        if self.frequency == "daily":
            gap = timedelta(days=1)
        elif self.frequency == "weekly":
            gap = timedelta(weeks=1)
        else:
            return None  # "once" tasks don't recur

        next_due = (self.due_date + gap) if self.due_date else None
        next_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            time=self.time,
            frequency=self.frequency,
            due_date=next_due,
        )
        if self.pet is not None:
            self.pet.add_task(next_task)
        return next_task


class Owner:
    """Represents the pet owner, storing their pets, available time, and preferences."""

    def __init__(self, name: str, available_time: int, preferences: Optional[dict] = None):
        """Initialize an Owner with a name, daily available time in minutes, and optional preferences."""
        self.name: str = name
        self.available_time: int = available_time   # in minutes; single source of truth
        self.preferences: dict = preferences or {}
        self.pets: list[Pet] = []
        self.scheduler: Optional[Scheduler] = None  # linked scheduler

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's list if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def update_preferences(self, preferences: dict) -> None:
        """Merge new preference key-value pairs into the owner's existing preferences."""
        self.preferences.update(preferences)

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of all tasks across every pet owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Generates a prioritized daily care schedule based on the owner's available time."""

    def __init__(self, owner: Owner):
        """Initialize the Scheduler with a reference to the Owner."""
        self.owner: Owner = owner               # access available_time via owner.available_time
        self.generated_plan: list[Task] = []    # final ordered, filtered schedule output

    def generate_schedule(self) -> list[Task]:
        """Sort all tasks by priority, filter by available time, and store the result as the plan."""
        sorted_tasks = self._sort_tasks_by_priority()
        self.generated_plan = self._filter_tasks_by_time(sorted_tasks)
        return self.generated_plan

    def _sort_tasks_by_priority(self) -> list[Task]:
        """Return all owner tasks sorted from highest to lowest priority."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda task: task.priority, reverse=True)

    def _filter_tasks_by_time(self, sorted_tasks: list[Task]) -> list[Task]:
        """Select tasks greedily in priority order until the owner's available time is used up."""
        selected = []
        time_remaining = self.owner.available_time
        for task in sorted_tasks:
            if task.duration <= time_remaining:
                selected.append(task)
                time_remaining -= task.duration
        return selected

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for any tasks sharing the same scheduled time."""
        warnings = []
        time_groups: dict[str, list[Task]] = {}

        for task in self.owner.get_all_tasks():
            if task.time is not None:
                time_groups.setdefault(task.time, []).append(task)

        for time_slot, tasks in time_groups.items():
            if len(tasks) > 1:
                names = " and ".join(t.name for t in tasks)
                warnings.append(f"Conflict: {names} are both scheduled at {time_slot}")

        return warnings

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return all tasks belonging to the pet with the given name."""
        tasks = self.owner.get_all_tasks()
        return [t for t in tasks if t.pet is not None and t.pet.name == pet_name]

    def filter_by_completion(self, completed: bool) -> list[Task]:
        """Return tasks that are done (completed=True) or still pending (completed=False)."""
        tasks = self.owner.get_all_tasks()
        return [t for t in tasks if t.completed == completed]

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted ascending by scheduled start time ('HH:MM'); unscheduled tasks last."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time if t.time is not None else "99:99")

    def find_next_available_slot(self) -> str:
        """Return the next available start time (HH:MM) after all scheduled tasks end.
        If no tasks have a scheduled time, returns '00:00'."""
        scheduled = [t for t in self.owner.get_all_tasks() if t.time is not None]
        if not scheduled:
            return "00:00"

        latest_end_minutes = 0
        for task in scheduled:
            hours, mins = map(int, task.time.split(":"))
            end = hours * 60 + mins + task.duration
            if end > latest_end_minutes:
                latest_end_minutes = end

        return f"{latest_end_minutes // 60:02d}:{latest_end_minutes % 60:02d}"

    def explain_plan(self) -> str:
        """Return a human-readable summary of the generated schedule."""
        if not self.generated_plan:
            return "No schedule has been generated yet. Call generate_schedule() first."

        total_time = sum(task.duration for task in self.generated_plan)
        lines = [
            f"Schedule for {self.owner.name}:",
            f"Available time: {self.owner.available_time} minutes",
            f"Tasks scheduled: {len(self.generated_plan)} (uses {total_time} minutes)",
            "",
        ]
        for i, task in enumerate(self.generated_plan, start=1):
            pet_name = task.pet.name if task.pet else "Unknown"
            lines.append(
                f"  {i}. [{task.category}] {task.name} for {pet_name}"
                f" — {task.duration} min (priority: {task.priority})"
            )
        return "\n".join(lines)
