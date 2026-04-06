import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task


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
