from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    name: str
    type: str
    age: int
    special_notes: str = ""

    def update_info(self, info: dict) -> None:
        pass


@dataclass
class Task:
    name: str
    duration: int       # in minutes
    priority: int
    category: str
    pet: Pet = None     # the pet this task belongs to
    completed: bool = False

    def update_task(
        self,
        name: Optional[str] = None,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
        category: Optional[str] = None,
    ) -> None:
        pass

    def mark_complete(self) -> None:
        pass


class Owner:
    def __init__(self, name: str, available_time: int, preferences: Optional[dict] = None):
        self.name: str = name
        self.available_time: int = available_time   # in minutes; single source of truth
        self.preferences: dict = preferences or {}
        self.pets: list[Pet] = []
        self.scheduler: Optional[Scheduler] = None  # linked scheduler

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: dict) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner           # access available_time via owner.available_time
        self.tasks: list[Task] = []         # input pool of all tasks
        self.generated_plan: list[Task] = []  # final ordered, filtered schedule output

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_schedule(self) -> list[Task]:
        # orchestrates _sort_tasks_by_priority() and _filter_tasks_by_time()
        pass

    def _sort_tasks_by_priority(self) -> list[Task]:
        pass

    def _filter_tasks_by_time(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
