from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime, date, time, timedelta

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

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Get tasks only for a specific pet."""
        return [task for task in self._all_tasks() if task.pet_name == pet_name]

    def get_tasks_by_status(self, is_complete: bool) -> List[Task]:
        """Filter tasks by completion status."""
        return [task for task in self._all_tasks() if task.completed == is_complete]

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self._all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by scheduled_time (earliest first)."""
        # Use `sorted(..., key=lambda t: t.scheduled_time)` with time objects
        return sorted([t for t in tasks if t.scheduled_time is not None], key=lambda t: t.scheduled_time)

    def get_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks as of today."""
        today = date.today()
        return [task for task in self._all_tasks() if task.is_overdue(today)]

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and create next occurrence for recurring tasks."""
        task.mark_complete()
        return self._create_next_occurrence(task)

    def _find_pet(self, pet_name: Optional[str]) -> Optional[Pet]:
        """Find a registered pet by name across all owners."""
        if not pet_name:
            return None
        for owner in self.owners:
            for pet in owner.pets:
                if pet.name == pet_name:
                    return pet
        return None

    def _create_next_occurrence(self, task: Task) -> Optional[Task]:
        """Create and append a new recurring task copy for the next date."""
        if task.frequency is None or task.frequency == Frequency.MONTHLY and task.scheduled_time is None:
            # non-recurring or no schedule; no auto-rolling task
            return None

        if task.frequency == Frequency.DAILY:
            next_date = date.today() + timedelta(days=1)
        elif task.frequency == Frequency.WEEKLY:
            next_date = date.today() + timedelta(weeks=1)
        elif task.frequency == Frequency.MONTHLY:
            next_date = date.today() + timedelta(days=30)
        else:
            return None

        new_task = Task(
            description=task.description,
            is_complete=False,
            scheduled_time=task.scheduled_time,
            frequency=task.frequency,
            pet_name=task.pet_name,
            owner_name=task.owner_name,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            due_date=next_date,
        )

        pet = self._find_pet(task.pet_name)
        if pet:
            pet.add_task(new_task)

        return new_task

    def _priority_rank(self, priority: str) -> int:
        """Lower number means higher urgency for sorting."""
        ranking = {"high": 0, "medium": 1, "low": 2}
        return ranking.get(priority, 1)

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect task conflicts and return warning messages (lightweight, non-crashing)."""
        warnings: List[str] = []
        sorted_tasks = sorted([t for t in tasks if t.scheduled_time is not None], key=lambda t: t.scheduled_time)

        for i in range(len(sorted_tasks) - 1):
            current = sorted_tasks[i]
            nxt = sorted_tasks[i + 1]
            if current.scheduled_time is None or nxt.scheduled_time is None:
                continue

            current_start = datetime.combine(date.today(), current.scheduled_time)
            current_end = current_start + timedelta(minutes=current.duration_minutes)
            next_start = datetime.combine(date.today(), nxt.scheduled_time)
            next_end = next_start + timedelta(minutes=nxt.duration_minutes)

            overlap = next_start < current_end
            same_time = current_start == next_start

            if overlap or same_time:
                pet_descr = "same pet" if current.pet_name == nxt.pet_name else "different pets"
                warning = (
                    f"Conflict: '{current.description}' ({current.pet_name}) at {current.scheduled_time.strftime('%H:%M')} "
                    f"and '{nxt.description}' ({nxt.pet_name}) at {nxt.scheduled_time.strftime('%H:%M')} - {pet_descr}."
                )
                warnings.append(warning)

        return warnings

    def _rollover_recurring_tasks(self, schedule_date: date) -> None:
        """Create next occurrence for completed recurring tasks and reset them."""
        for task in self._all_tasks():
            if task.frequency and task.completed:
                if task.frequency == Frequency.DAILY:
                    next_due = schedule_date + timedelta(days=1)
                elif task.frequency == Frequency.WEEKLY:
                    next_due = schedule_date + timedelta(weeks=1)
                elif task.frequency == Frequency.MONTHLY:
                    # rough monthly increment (~30 days)
                    next_due = schedule_date + timedelta(days=30)
                else:
                    continue

                task.due_date = next_due
                task.reset()

    def construct_task_schedule(
        self,
        schedule_date: date,
        day_start: time,
        day_end: time,
        pet_name: Optional[str] = None,
        include_completed: bool = False,
    ) -> List[Task]:
        """Return a schedule of tasks for the selected day and optional pet."""
        self._rollover_recurring_tasks(schedule_date)

        tasks = self._all_tasks()
        if pet_name:
            tasks = [t for t in tasks if t.pet_name == pet_name]

        if not include_completed:
            tasks = [t for t in tasks if not t.completed]

        time_candidates = [t for t in tasks if t.scheduled_time is not None]
        time_candidates.sort(key=lambda t: (t.scheduled_time, self._priority_rank(t.priority)))

        selected = []
        current_end = datetime.combine(schedule_date, day_start)
        for task in time_candidates:
            task_start = datetime.combine(schedule_date, task.scheduled_time)
            task_end = task_start + timedelta(minutes=task.duration_minutes)
            if day_start <= task.scheduled_time <= day_end and task_start >= current_end:
                selected.append(task)
                current_end = task_end

        return selected

    def explain_schedule(self, tasks: List[Task]) -> str:
        """Return a textual explanation of a list of scheduled tasks."""
        lines = []
        for task in tasks:
            scheduled = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
            lines.append(f"{task.owner_name}/{task.pet_name}: {task.description} at {scheduled} ({task.priority})")
        return "\n".join(lines)
