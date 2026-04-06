import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


def test_mark_complete():
    task = Task(name="Morning Walk", duration=30, priority=3, category="Exercise")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(name="Max", type="Dog", age=3)
    task = Task(name="Feed Max", duration=10, priority=5, category="Feeding")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task


def test_sort_by_time():
    owner = Owner(name="Alex", available_time=120)
    pet = Pet(name="Max", type="Dog", age=3)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    task_a = Task(name="Evening Walk", duration=30, priority=2, category="Exercise", time="18:00")
    task_b = Task(name="Lunch Feed", duration=10, priority=3, category="Feeding", time="12:00")
    task_c = Task(name="Morning Walk", duration=20, priority=5, category="Exercise", time="08:00")

    pet.add_task(task_a)
    pet.add_task(task_b)
    pet.add_task(task_c)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].time == "08:00"
    assert sorted_tasks[1].time == "12:00"
    assert sorted_tasks[2].time == "18:00"


def test_recurrence_daily():
    owner = Owner(name="Alex", available_time=120)
    pet = Pet(name="Luna", type="Cat", age=2)
    owner.add_pet(pet)

    today = date(2026, 4, 5)
    task = Task(
        name="Feed Luna",
        duration=10,
        priority=4,
        category="Feeding",
        frequency="daily",
        due_date=today,
    )
    pet.add_task(task)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task in pet.tasks


def test_detect_conflicts():
    owner = Owner(name="Alex", available_time=120)
    pet = Pet(name="Max", type="Dog", age=3)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    task_a = Task(name="Feed Max", duration=10, priority=5, category="Feeding", time="08:00")
    task_b = Task(name="Vet Visit", duration=60, priority=3, category="Health", time="08:00")

    pet.add_task(task_a)
    pet.add_task(task_b)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
