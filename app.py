from pawpal_system import Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Initialize session state ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

owner = st.session_state.owner

# --- Owner Settings ---
st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col2:
    owner.available_time = st.number_input(
        "Available time (minutes)", min_value=1, max_value=480, value=owner.available_time
    )

st.divider()

# --- Add a Pet ---
st.subheader("Pets")

with st.form("add_pet_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        pet_type = st.selectbox("Species", ["Dog", "Cat", "Other"])
    with col3:
        pet_age = st.number_input("Age", min_value=0, max_value=30, value=2)
    pet_notes = st.text_input("Special notes (optional)", value="")
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    new_pet = Pet(name=pet_name, type=pet_type, age=pet_age, special_notes=pet_notes)
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name} to {owner.name}'s pets.")

if owner.pets:
    st.write("Current pets:")
    st.table([
        {"Name": p.name, "Type": p.type, "Age": p.age, "Notes": p.special_notes}
        for p in owner.pets
    ])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("Tasks")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox(
            "Assign to pet", options=[p.name for p in owner.pets]
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            task_name = st.text_input("Task name", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.number_input("Priority (1–10)", min_value=1, max_value=10, value=5)
        category = st.text_input("Category", value="Exercise")
        add_task = st.form_submit_button("Add task")

    if add_task:
        target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
        new_task = Task(name=task_name, duration=int(duration), priority=int(priority), category=category)
        target_pet.add_task(new_task)
        st.success(f"Added '{task_name}' to {selected_pet_name}'s tasks.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([
            {
                "Task": t.name,
                "Pet": t.pet.name if t.pet else "—",
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Category": t.category,
                "Done": t.completed,
            }
            for t in all_tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        plan = scheduler.generate_schedule()
        if plan:
            st.success(f"Schedule generated — {len(plan)} task(s) fit in {owner.available_time} minutes.")
            st.table([
                {
                    "Task": t.name,
                    "Pet": t.pet.name if t.pet else "—",
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Category": t.category,
                }
                for t in plan
            ])
            st.text(scheduler.explain_plan())
        else:
            st.warning("No tasks fit within the available time.")
