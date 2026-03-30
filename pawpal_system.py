from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime, date, time

class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    description: str
    is_complete: bool = False
    scheduled_time: Optional[time] = None
    frequency: Optional[Frequency] = None
    pet_name: Optional[str] = None
    owner_name: Optional[str] = None
    duration_minutes: int = 15
    priority: str = "medium"  # low|medium|high
    due_date: Optional[date] = None

    @property
    def completed(self) -> bool:
        """Return whether the task is marked complete."""
        return self.is_complete

    @completed.setter
    def completed(self, value: bool) -> None:
        """Set the task completion status."""
        self.is_complete = value

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.is_complete = True

    def reset(self) -> None:
        """Reset the task to incomplete."""
        self.is_complete = False

    def is_overdue(self, today: Optional[date] = None) -> bool:
        """Check whether the task is overdue compared to a date."""
        if self.due_date is None:
            return False
        if today is None:
            today = date.today()
        return not self.completed and self.due_date < today


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        self.tasks = [t for t in self.tasks if t is not task]

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        self.pets = [p for p in self.pets if p is not pet]

    def get_all_tasks(self) -> List[Task]:
        """Collect all tasks across this owner’s pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    def __init__(self):
        self.owners: List[Owner] = []

    def add_owner(self, owner: Owner) -> None:
        """Register an owner with the scheduler."""
        self.owners.append(owner)

    def _all_tasks(self) -> List[Task]:
        """Return the list of all tasks available in the scheduler."""
        tasks: List[Task] = []
        for owner in self.owners:
            tasks.extend(owner.get_all_tasks())
        return tasks

    def get_tasks_by_frequency(self, frequency: Frequency) -> List[Task]:
        """Get tasks filtered by a frequency value."""
        return [task for task in self._all_tasks() if task.frequency == frequency]

    def get_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks as of today."""
        today = date.today()
        return [task for task in self._all_tasks() if task.is_overdue(today)]

    def complete_task(self, task: Task) -> None:
        """Mark a task complete via scheduler action."""
        task.mark_complete()

    def generate_daily_schedule(self, schedule_date: date, day_start: time, day_end: time) -> List[Task]:
        """Generate a daily schedule of eligible tasks between start and end."""
        candidates = [task for task in self._all_tasks() if not task.completed and not task.is_overdue(schedule_date)]
        candidates.sort(key=lambda t: (t.priority == 'high', t.scheduled_time))
        daily = [task for task in candidates if day_start <= task.scheduled_time <= day_end]
        return daily

    def explain_schedule(self, tasks: List[Task]) -> str:
        """Return a textual explanation of a list of scheduled tasks."""
        lines = []
        for task in tasks:
            lines.append(f"{task.owner_name}/{task.pet_name}: {task.description} at {task.scheduled_time} ({task.priority})")
        return "\n".join(lines)
