from dataclasses import dataclass
from typing import List
from enum import Enum

class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    description: str
    time: str
    frequency: Frequency
    completed: bool = False

    def mark_complete(self) -> None:
        ...

    def reset(self) -> None:
        ...


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task]

    def add_task(self, task: Task) -> None:
        ...

    def remove_task(self, task: Task) -> None:
        ...

    def get_pending_tasks(self) -> List[Task]:
        ...


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        ...

    def remove_pet(self, pet: Pet) -> None:
        ...

    def get_all_tasks(self) -> List[Task]:
        ...


class Scheduler:
    def __init__(self):
        self.owners: List[Owner] = []

    def add_owner(self, owner: Owner) -> None:
        ...

    def get_tasks_by_frequency(self, frequency: Frequency) -> List[Task]:
        ...

    def get_overdue_tasks(self) -> List[Task]:
        ...

    def complete_task(self, task: Task) -> None:
        ...