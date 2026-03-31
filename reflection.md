# PawPal+ Project Reflection

## 1. System Design
Three tasks that a user should do is to be able to track pet care tasks, enter user and pet information, and view a daily produce a daily plan.
**a. Initial design**

- Briefly describe your initial UML d#coesign.
- What classes did you include, and what responsibilities did you assign to each?
I designed four main classes: Task, Pet, Owner, and Scheduler. The Task class represents individual activities such as feeding or walking, storing details like time, frequency, and completion status. The Pet class manages information about each pet and maintains a list of its tasks. The Owner class represents the user and holds multiple pets, providing access to all tasks across them. The Scheduler acts as the central controller, organizing, sorting, and managing tasks from all pets to generate a daily schedule.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
yes, I removed task resolution ambiguity by making task know owner/pet context, avoided repeated nested scans with _all_tasks() aggregator, added direct frequency/overdue queries.
lastly, added schedule generation flow and explanation helper.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- The scheduler currently detects conflicts via exact time overlap in `Scheduler.detect_conflicts()` (same start or direct overlap in minutes), but it does not attempt full multi-segment interval packing or sliding window reassignments.
- This is a deliberate tradeoff for readability and predictable behavior: it provides a lightweight warning mechanism without trying to solve NP-hard schedule optimization. A more aggressive strategy could improve utilization, but it would also require more complex algorithms and may reduce transparency for users.

---

## 3. AI Collaboration

**a. How you used AI**

- I used Copilot for design brainstorming to map out the Scheduler class responsibilities and to generate method stubs that fit the use cases. I used it for code generation when translating requirements into methods for sorting, filtering, conflict detection, and recurrence. I also used it for debugging and test generation, quickly verifying assumptions with pytest and adjusting logic.
- Prompts that asked for focused functionality ('sort tasks by time', 'recurring task rollover', 'conflict warning') were most helpful.

**b. Judgment and verification**

- I rejected an early AI suggestion that tried to solve scheduling with a very complex global optimization candidate set (NP-hard), because this was overkill for the project scope. Instead, I kept a deterministic approach (greedy window scheduling, explicit conflict warnings) for clarity and faster implementation.
- I verified by writing tests for each behavior and running `python -m pytest` frequently. When an AI-generated implementation didn't match expected output, I rewrote that path manually.

**c. Copilot features**

- Inline suggestions and code completions helped build methods quickly (e.g., generating `detect_conflicts` loops). The generated test scaffolding was valuable for fast feedback.
- Using separate chat sessions for phases (design, implementation, testing) kept the work organized and reduced context-switching complexity.
- Being the 'lead architect' meant accepting AI's best ideas when they matched project constraints, otherwise pruning them for simplicity and maintainability.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
