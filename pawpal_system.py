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
    duration: int  # in minutes
    priority: int
    category: str
    completed: bool = False

    def update_task(self, info: dict) -> None:
        pass

    def mark_complete(self) -> None:
        pass


class Owner:
    def __init__(self, name: str, available_time: int, preferences: Optional[dict] = None):
        self.name: str = name
        self.available_time: int = available_time  # in minutes
        self.preferences: dict = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: dict) -> None:
        pass


class Scheduler:
    def __init__(self, available_time: int):
        self.available_time: int = available_time  # in minutes
        self.tasks: list[Task] = []
        self.generated_plan: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def generate_schedule(self) -> list[Task]:
        pass

    def sort_tasks_by_priority(self) -> list[Task]:
        pass

    def filter_tasks_by_time(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
