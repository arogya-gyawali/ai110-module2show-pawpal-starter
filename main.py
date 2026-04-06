from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # --- Setup Owner ---
    owner = Owner(name="Alex", available_time=120)

    # --- Create Pets ---
    dog = Pet(name="Max", type="Dog", age=3)
    cat = Pet(name="Luna", type="Cat", age=5, special_notes="Needs medication after meals")

    owner.add_pet(dog)
    owner.add_pet(cat)

    # --- Create Tasks ---
    morning_walk = Task(name="Morning Walk",   duration=30, priority=3, category="Exercise")
    feeding_dog  = Task(name="Feed Max",       duration=10, priority=5, category="Feeding")
    feeding_cat  = Task(name="Feed Luna",      duration=10, priority=5, category="Feeding")
    medication   = Task(name="Give Medication",duration=5,  priority=4, category="Health")
    grooming     = Task(name="Brush Coat",     duration=20, priority=2, category="Grooming")
    playtime     = Task(name="Playtime",       duration=30, priority=1, category="Exercise")

    # --- Assign Tasks to Pets ---
    dog.add_task(morning_walk)
    dog.add_task(feeding_dog)
    dog.add_task(grooming)
    dog.add_task(playtime)

    cat.add_task(feeding_cat)
    cat.add_task(medication)

    # --- Run Scheduler ---
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_schedule()

    # --- Print Schedule ---
    print("=" * 40)
    print("        TODAY'S SCHEDULE")
    print("=" * 40)

    for i, task in enumerate(plan, start=1):
        pet_name = task.pet.name if task.pet else "Unknown"
        print(f"{i}. {task.name}")
        print(f"   Pet:      {pet_name}")
        print(f"   Duration: {task.duration} min")
        print(f"   Priority: {task.priority}")
        print()

    print("-" * 40)
    print(scheduler.explain_plan())
    print("=" * 40)


if __name__ == "__main__":
    main()
