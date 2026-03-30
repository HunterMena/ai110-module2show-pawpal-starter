from pawpal_system import Owner, Pet, Task
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
    "Morning Walk",
    datetime.now().replace(hour=8, minute=0).time(),
    Frequency.DAILY,
    pet1.name,
    owner.name,
    duration_minutes=30,
    priority="high",
)
task2 = Task(
    "Feeding Time",
    datetime.now().replace(hour=12, minute=0).time(),
    Frequency.DAILY,
    pet2.name,
    owner.name,
    duration_minutes=15,
    priority="medium",
)
task3 = Task(
    "Playtime",
    datetime.now().replace(hour=18, minute=30).time(),
    Frequency.DAILY,
    pet1.name,
    owner.name,
    duration_minutes=20,
    priority="low",
)

# Add tasks to pets
pet1.add_task(task1)
pet2.add_task(task2)
pet1.add_task(task3)

# Print Today's Schedule
print("=" * 50)
print("TODAY'S SCHEDULE")
print("=" * 50)
print(f"Owner: {owner.name}\n")

for pet in owner.pets:
    print(f"Pet: {pet.name} ({pet.species})")
    for task in sorted(pet.tasks, key=lambda t: t.scheduled_time):
        print(f"  - {task.description} at {task.scheduled_time.strftime('%H:%M')} ({task.priority})")
    print()