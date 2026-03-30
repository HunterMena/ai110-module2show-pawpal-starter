const mermaidDiagram = `
classDiagram
    class Owner {
        +int owner_id;
        +string name;
        +string email;
        +string phone;
        +List~Pet~ pets;
        +create_pet(name, species, age);
        +add_pet(pet);
        +remove_pet(pet_id);
        +get_pets();
        +get_preferences();
    }

    class Pet {
        +int pet_id;
        +string name;
        +string species;
        +int age;
        +string breed;
        +string diet_info;
        +List~Task~ tasks;
        +add_task(task);
        +remove_task(task_id);
        +get_tasks();
        +get_care_profile();
    }

    class Task {
        +int task_id;
        +string title;
        +string description;
        +int duration_minutes;
        +date due_date;
        +string priority;
        +string status;
        +int pet_id;
        +int owner_id;
        +string location;
        +set_status(status);
        +is_overdue();
        +estimated_endtime(start_time);
    }

    class Scheduler {
        +int scheduler_id;
        +Owner owner;
        +List~Task~ tasks;
        +date schedule_date;
        +List~ScheduledItem~ schedule;
        +add_task(task);
        +remove_task(task_id);
        +load_owner_tasks(owner, date=None);
        +generate_schedule(day_start, day_end, preferences);
        +_score_task(task, preferences);
        +_sort_tasks();
        +export_schedule(format);
        +explain_schedule();
    }

    Owner "1" --> "*" Pet : owns;
    Pet "1" --> "*" Task : has;
    Scheduler "1" --> "1" Owner : schedules for;
    Scheduler "1" --> "*" Task : arranges;
`;

export default mermaidDiagram;
