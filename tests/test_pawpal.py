import pytest
from datetime import date, time, timedelta
from pawpal import Owner, Pet, Task, Scheduler, Frequency


def test_mark_complete_changes_status():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task("Feed dog", False)
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_adding_task_increases_pet_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet("Buddy", "Dog")
    initial_count = len(pet.tasks)

    task = Task("Walk", False)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_scheduler_sort_tasks_by_time():
    """Verify tasks are returned in chronological order."""
    owner = Owner("Alice")
    pet = Pet("Buddy", "Dog")
    owner.add_pet(pet)

    t1 = Task(description="Lunch", scheduled_time=time(hour=12, minute=0), priority="medium")
    t2 = Task(description="Morning Walk", scheduled_time=time(hour=8, minute=0), priority="high")
    t3 = Task(description="Playtime", scheduled_time=time(hour=18, minute=0), priority="low")

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)

    scheduler = Scheduler()
    scheduler.add_owner(owner)
    sorted_tasks = scheduler.sort_tasks_by_time(pet.tasks)

    assert [t.description for t in sorted_tasks] == ["Morning Walk", "Lunch", "Playtime"]


def test_scheduler_completion_rolls_over_daily_task():
    """Confirm that marking a daily task complete creates next occurrence."""
    owner = Owner("Alice")
    pet = Pet("Buddy", "Dog")
    owner.add_pet(pet)

    task = Task(
        description="Feed dog",
        is_complete=False,
        scheduled_time=time(hour=9, minute=0),
        frequency=Frequency.DAILY,
        pet_name=pet.name,
        owner_name=owner.name,
    )

    pet.add_task(task)
    scheduler = Scheduler()
    scheduler.add_owner(owner)

    new_task = scheduler.complete_task(task)

    assert task.completed is True
    assert new_task is not None
    assert new_task.pet_name == pet.name
    assert new_task.frequency == Frequency.DAILY
    assert new_task.due_date == date.today() + timedelta(days=1)


def test_scheduler_conflict_detection_for_exact_duplicate_time():
    """Verify Scheduler flags duplicate exact times as a conflict warning."""
    owner = Owner("Alice")
    pet = Pet("Buddy", "Dog")
    owner.add_pet(pet)

    t1 = Task(description="Groom", scheduled_time=time(hour=9, minute=0), duration_minutes=30, pet_name=pet.name)
    t2 = Task(description="Vet", scheduled_time=time(hour=9, minute=0), duration_minutes=30, pet_name=pet.name)

    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = Scheduler()
    scheduler.add_owner(owner)

    conflicts = scheduler.detect_conflicts(pet.tasks)

    assert len(conflicts) > 0
    assert "Conflict" in conflicts[0]
