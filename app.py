from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler, Frequency
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

state = st.session_state

if "owner" not in state:
    state["owner"] = Owner(owner_name)

if "pets" not in state:
    state["pets"] = []

if "tasks" not in state:
    state["tasks"] = []

if "current_pet" not in state:
    state["current_pet"] = None

if "scheduler" not in state:
    state["scheduler"] = Scheduler()
    state["scheduler"].add_owner(state["owner"])

if "schedule_results" not in state:
    state["schedule_results"] = []

if "conflicts" not in state:
    state["conflicts"] = []

# Add a pet object to backend state via Owner.add_pet()
if st.button("Add pet"):
    state["owner"].name = owner_name
    new_pet = Pet(pet_name, species)
    state["owner"].add_pet(new_pet)
    state["pets"].append(new_pet)
    state["current_pet"] = new_pet
    state["scheduler"].add_owner(state["owner"])

if state["pets"]:
    pet_names = [p.name for p in state["pets"]]
    selected_pet = st.selectbox("Current pet", pet_names, index=pet_names.index(state["current_pet"].name) if state["current_pet"] else 0)
    state["current_pet"] = next((p for p in state["pets"] if p.name == selected_pet), state["current_pet"])
else:
    state["current_pet"] = None

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in state:
    state["tasks"] = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    scheduled_time = st.time_input("Scheduled time", value=datetime.now().time())

frequency = st.selectbox("Recurrence", ["none", "daily", "weekly", "monthly"], index=0)
frequency_value = None
if frequency == "daily":
    frequency_value = Frequency.DAILY
elif frequency == "weekly":
    frequency_value = Frequency.WEEKLY
elif frequency == "monthly":
    frequency_value = Frequency.MONTHLY

if st.button("Add task"):
    task = Task(
        description=task_title,
        is_complete=False,
        scheduled_time=scheduled_time,
        frequency=frequency_value,
        pet_name=state["current_pet"].name if state["current_pet"] else None,
        owner_name=state["owner"].name,
        duration_minutes=int(duration),
        priority=priority,
    )

    if state["current_pet"] is not None:
        state["current_pet"].add_task(task)
        state["tasks"].append(task)
    else:
        st.warning("Please add a pet before adding tasks.")

if state["current_pet"] and state["current_pet"].tasks:
    st.write(f"Current tasks for {state['current_pet'].name}:")
    st.table([
        {
            "description": t.description,
            "complete": t.completed,
            "duration": t.duration_minutes,
            "priority": t.priority,
        }
        for t in state["current_pet"].tasks
    ])
elif state["tasks"]:
    st.write("All tasks in session:")
    st.table([
        {
            "description": t.description,
            "pet": t.pet_name,
            "owner": t.owner_name,
            "complete": t.completed,
            "duration": t.duration_minutes,
            "priority": t.priority,
        }
        for t in state["tasks"]
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule for selected pet or all pets")

schedule_date = st.date_input("Schedule date", value=date.today())
day_start = st.time_input("Day start", value=datetime.strptime("08:00", "%H:%M").time())
day_end = st.time_input("Day end", value=datetime.strptime("17:00", "%H:%M").time())
filter_pet = st.selectbox("Filter by pet", ["all"] + [p.name for p in state["pets"]], index=0)
include_completed = st.checkbox("Include completed tasks", value=False)

if st.button("Generate schedule"):
    pet_filter_name = None if filter_pet == "all" else filter_pet
    state["schedule_results"] = state["scheduler"].construct_task_schedule(
        schedule_date=schedule_date,
        day_start=day_start,
        day_end=day_end,
        pet_name=pet_filter_name,
        include_completed=include_completed,
    )
    state["conflicts"] = state["scheduler"].detect_conflicts(state["schedule_results"])

if state["schedule_results"]:
    st.write("### Scheduled tasks")
    st.table([
        {
            "description": t.description,
            "pet": t.pet_name,
            "time": t.scheduled_time.strftime("%H:%M") if t.scheduled_time else "--",
            "duration": t.duration_minutes,
            "priority": t.priority,
            "completed": t.completed,
        }
        for t in state["schedule_results"]
    ])
else:
    st.info("No scheduled tasks for selected date/window yet. Add tasks and click Generate schedule.")

if state["conflicts"]:
    st.warning("Conflicts detected in your schedule. Resolve these tasks to avoid missed pet care events:")
    for conflict_text in state["conflicts"]:
        st.warning(conflict_text)
    st.info("Try adjusting times or setting different priorities to avoid overlap.")


