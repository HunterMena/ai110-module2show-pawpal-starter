import pytest
from pawpal import Pet, Task

def test_mark_complete_changes_status():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task("Feed dog", False)
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_adding_task_increases_pet_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet("Buddy", "Dog")
    initial_count = len(pet.tasks) if hasattr(pet, 'tasks') else 0
    
    task = Task("Walk", False)
    pet.add_task(task)
    
    assert len(pet.tasks) == initial_count + 1