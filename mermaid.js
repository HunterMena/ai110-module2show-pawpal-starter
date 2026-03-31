const mermaidDiagram = `
classDiagram
    class Owner {
        +string name
        +List~Pet~ pets
        +add_pet(pet)
        +remove_pet(pet)
        +get_all_tasks()
    }

    class Pet {
        +string name
        +string species
        +List~Task~ tasks
        +add_task(task)
        +remove_task(task)
        +get_pending_tasks()
    }

    class Task {
        +string description
        +bool is_complete
        +time scheduled_time
        +Frequency frequency
        +string pet_name
        +string owner_name
        +int duration_minutes
        +string priority
        +date due_date
        +mark_complete()
        +reset()
        +is_overdue(today)
    }

    class Scheduler {
        +List~Owner~ owners
        +add_owner(owner)
        +get_tasks_by_frequency(frequency)
        +get_tasks_for_pet(pet_name)
        +get_tasks_by_status(is_complete)
        +filter_tasks(pet_name, completed)
        +sort_tasks_by_time(tasks)
        +get_overdue_tasks()
        +complete_task(task)
        +detect_conflicts(tasks)
        +construct_task_schedule(schedule_date, day_start, day_end, pet_name, include_completed)
    }

    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler "1" --> "*" Owner : manages
    Scheduler "1" --> "*" Task : schedules

`;

export default mermaidDiagram;
