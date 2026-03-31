from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

# Create an Owner
owner = Owner("Alice")

# Create at least two Pets
pet1 = Pet("Buddy", "Dog")
pet2 = Pet("Whiskers", "Cat")

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

from pawpal_system import Frequency

# Create tasks with different times
task1 = Task(
    description="Morning Walk",
    is_complete=False,
    scheduled_time=datetime.now().replace(hour=8, minute=0).time(),
    frequency=Frequency.DAILY,
    pet_name=pet1.name,
    owner_name=owner.name,
    duration_minutes=30,
    priority="high",
)
task2 = Task(
    description="Feeding Time",
    is_complete=False,
    scheduled_time=datetime.now().replace(hour=12, minute=0).time(),
    frequency=Frequency.DAILY,
    pet_name=pet2.name,
    owner_name=owner.name,
    duration_minutes=15,
    priority="medium",
)
task3 = Task(
    description="Playtime",
    is_complete=False,
    scheduled_time=datetime.now().replace(hour=18, minute=30).time(),
    frequency=Frequency.DAILY,
    pet_name=pet1.name,
    owner_name=owner.name,
    duration_minutes=20,
    priority="low",
)

# Add tasks to pets
pet1.add_task(task1)
pet2.add_task(task2)
pet1.add_task(task3)

# Add conflict tasks (same time) for testing
conflict_task_a = Task(
    description="Vet check",
    is_complete=False,
    scheduled_time=datetime.now().replace(hour=9, minute=0).time(),
    frequency=Frequency.DAILY,
    pet_name=pet1.name,
    owner_name=owner.name,
    duration_minutes=30,
    priority="high",
)
conflict_task_b = Task(
    description="Grooming",
    is_complete=False,
    scheduled_time=datetime.now().replace(hour=9, minute=0).time(),
    frequency=Frequency.DAILY,
    pet_name=pet1.name,
    owner_name=owner.name,
    duration_minutes=30,
    priority="medium",
)
pet1.add_task(conflict_task_a)
pet1.add_task(conflict_task_b)

# Print Today's Schedule
print("=" * 50)
print("TODAY'S SCHEDULE")
print("=" * 50)
print(f"Owner: {owner.name}\n")

# Print unsorted tasks to show order creation
print("UNSORTED TASKS by creation order")
for pet in owner.pets:
    print(f"Pet: {pet.name} ({pet.species})")
    for task in pet.tasks:
        print(f"  - {task.description} at {task.scheduled_time.strftime('%H:%M')} ({task.priority})")
    print()

# Sort tasks by time using Scheduler.sort_tasks_by_time
scheduler = Scheduler()
scheduler.add_owner(owner)
all_tasks = owner.get_all_tasks()
sorted_tasks = scheduler.sort_tasks_by_time(all_tasks)
print("SORTED TASKS (by scheduled_time)")
for task in sorted_tasks:
    print(f"  - {task.description} at {task.scheduled_time.strftime('%H:%M')} ({task.priority})")
print()

# Filter tasks by pet and status
pet_filter = "Buddy"
filtered_tasks = scheduler.filter_tasks(pet_name=pet_filter, completed=False)
print(f"FILTERED TASKS for pet={pet_filter}, completed=False")
for task in filtered_tasks:
    print(f"  - {task.description} at {task.scheduled_time.strftime('%H:%M')} ({task.priority})")
print()

# Conflicts detection
conflicts = scheduler.detect_conflicts(sorted_tasks)
print("CONFLICTS:")
if not conflicts:
    print("  none")
else:
    for warning in conflicts:
        print(f"  {warning}")