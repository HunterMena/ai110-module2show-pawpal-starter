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

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
