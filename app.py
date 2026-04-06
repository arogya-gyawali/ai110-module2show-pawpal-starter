from pawpal_system import Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Initialize session state ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=120)

owner = st.session_state.owner

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🐾 PawPal+")
st.caption("Plan your pet's daily care — organized by priority, time, and availability.")
st.divider()

# ════════════════════════════════════════════════════════════════════════════
# STEP 1 — Owner
# ════════════════════════════════════════════════════════════════════════════
st.subheader("Step 1 · Owner Settings")
col1, col2 = st.columns(2)
with col1:
    owner.name = st.text_input("Your name", value=owner.name)
with col2:
    owner.available_time = st.number_input(
        "Daily available time (minutes)", min_value=1, max_value=480,
        value=owner.available_time
    )

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# STEP 2 — Pets
# ════════════════════════════════════════════════════════════════════════════
st.subheader("Step 2 · Your Pets")

with st.expander("➕ Add a new pet", expanded=not owner.pets):
    with st.form("add_pet_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            pet_name = st.text_input("Pet name", placeholder="e.g. Mochi")
        with col2:
            pet_type = st.selectbox("Species", ["Dog", "Cat", "Other"])
        with col3:
            pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
        pet_notes = st.text_input("Special notes (optional)", placeholder="e.g. needs allergy meds")
        add_pet = st.form_submit_button("Add Pet", use_container_width=True)

    if add_pet and pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), type=pet_type, age=pet_age, special_notes=pet_notes))
        st.success(f"{pet_name} added!")
    elif add_pet:
        st.error("Pet name cannot be empty.")

if owner.pets:
    pet_icon = {"Dog": "🐕", "Cat": "🐈"}
    st.table([
        {
            "Pet": f"{pet_icon.get(p.type, '🐾')} {p.name}",
            "Species": p.type,
            "Age": f"{p.age}y",
            "Tasks": len(p.tasks),
            "Notes": p.special_notes or "—",
        }
        for p in owner.pets
    ])
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# STEP 3 — Tasks
# ════════════════════════════════════════════════════════════════════════════
st.subheader("Step 3 · Tasks")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.expander("➕ Add a new task", expanded=not owner.get_all_tasks()):
        with st.form("add_task_form", clear_on_submit=True):
            selected_pet_name = st.selectbox("Assign to pet", options=[p.name for p in owner.pets])
            col1, col2 = st.columns(2)
            with col1:
                task_name = st.text_input("Task name", placeholder="e.g. Morning walk")
            with col2:
                category = st.text_input("Category", placeholder="e.g. Exercise")
            col3, col4, col5 = st.columns(3)
            with col3:
                duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
            with col4:
                priority = st.slider("Priority (1–10)", min_value=1, max_value=10, value=5)
            with col5:
                task_time = st.text_input("Time (HH:MM)", placeholder="Optional")
            add_task = st.form_submit_button("Add Task", use_container_width=True)

        if add_task and task_name.strip():
            target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
            target_pet.add_task(Task(
                name=task_name.strip(),
                duration=int(duration),
                priority=int(priority),
                category=category.strip() or "General",
                time=task_time.strip() if task_time.strip() else None,
            ))
            st.success(f"'{task_name}' added to {selected_pet_name}.")
        elif add_task:
            st.error("Task name cannot be empty.")

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        scheduler = Scheduler(owner=owner)
        sorted_tasks = scheduler.sort_by_time()

        st.caption(f"{len(all_tasks)} task(s) · sorted by scheduled time")
        st.table([
            {
                "Task": t.name,
                "Pet": t.pet.name if t.pet else "—",
                "Time": t.time if t.time else "—",
                "Duration (min)": t.duration,
                "Priority": t.priority,
                "Category": t.category,
                "Done": "Yes" if t.completed else "No",
            }
            for t in sorted_tasks
        ])

        # Conflicts inline, right below the task list
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.markdown("**Scheduling conflicts detected:**")
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts.")
    else:
        st.info("No tasks yet.")

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# STEP 4 — Generate Schedule
# ════════════════════════════════════════════════════════════════════════════
st.subheader("Step 4 · Generate Schedule")

all_tasks = owner.get_all_tasks()
if not all_tasks:
    st.info("Complete Steps 2 and 3 first.")
else:
    if st.button("Generate Schedule", type="primary", use_container_width=True):
        scheduler = Scheduler(owner=owner)
        plan = scheduler.generate_schedule()
        if plan:
            total_used = sum(t.duration for t in plan)
            skipped = len(all_tasks) - len(plan)

            col1, col2, col3 = st.columns(3)
            col1.metric("Tasks scheduled", len(plan))
            col2.metric("Time used", f"{total_used} min")
            col3.metric("Tasks skipped", skipped)

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

            with st.expander("View full plan explanation"):
                st.text(scheduler.explain_plan())
        else:
            st.warning(
                "No tasks fit within your available time. "
                "Try increasing your available time or reducing task durations."
            )
