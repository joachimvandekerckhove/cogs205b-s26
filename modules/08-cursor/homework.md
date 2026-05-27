# Homework -- ABM capstone with AI-assisted workflow

## Purpose

- Build and analyze an agent-based model using AI-assisted coding.
- Use a rigorous scientific workflow from planning through verification.
- Use at least one context-management tool (a skill or subagent). 
- Write a short reflection on how you ensured accuracy of the codebase (at most 250 words).

## Project scope

Implement any agent-based model simulation that you find interesting.

The project should include multiple files and at least one nontrivial design decision about coding agent rules, environment, or measurements.

The project should test one scientific hypothesis about the model. The hypothesis should compare at least two parameter settings, mechanisms, or interaction structures. For example: "Lower tolerance will produce higher polarization", or "Agents with memory decay will preserve rumors less accurately than agents without decay."

Suitable project types include:

- opinion dynamics or polarization
- diffusion of a behavioral norm
- category learning with interacting agents
- spreading of activation among neurons
- foraging or exploration strategy competition
- collective memory or rumor distortion
- benefits of metacognition or self-monitoring
- ...

Keep the model small enough that you can explain and verify it.

## Workflow

- [ ] Write a detailed prompt for the AI to plan the project. Save it as `PROMPT.md`.
- [ ] Use bounded prompts with explicit constraints and verification commands.
- [ ] Use at least one context-management tool (a skill or subagent). 
- [ ] Include at least one verification strategy specific to simulations (see below).
- [ ] Plan to test one hypothesis about the model.
- [ ] Use Plan mode, then curate and save the plan artifact (you can find it in the `~/.cursor/plans/` folder) as `PLAN.md`.
- [ ] Have the AI write the code to implement the plan.
- [ ] Confirm that the code is correct as intended.
- [ ] You are responsible for the scientific conclusions. The AI will help express, implement, or test them, but you must decide whether the results make theoretical sense.

## Verification examples

Include at least one simulation-specific verification strategy, such as:

- invariant checks: beliefs remain in bounds, population size stays constant, probabilities sum to 1
- deterministic seed checks: the same seed gives the same result
- edge-case checks: zero agents, one agent, no interaction, no learning, extreme parameter values
- ablation checks: remove a mechanism and confirm the expected qualitative change
- sensitivity checks: run several seeds or parameter settings and summarize variability

## Context-management tool

A skill or subagent should help the AI preserve project-specific context across prompts. Don't just restate the prompt or assignment -- use it to encode useful/relevant project knowledge, such as model assumptions, file structure, verification rules, coding conventions, or common failure modes detectable in testing.  You may of course use multiple skills and subagents!

## Deliverables: next week

A 5-10 minute in-class presentation of your project idea. Include:

- research question / hypothesis about a planned comparison, ablation, or parameter contrast
- model assumptions and update rules
- expected qualitative behavior
- verification strategy
- one thing that would make you distrust the model result
- draft of the initial prompt you used to describe the project to the AI for planning purposes

We will use this presentation to help you refine your project idea and prompt.

## Deliverables: Final

By the Wednesday of Finals week, submit an `abm-project/` folder with:

- `PROMPT.md` containing the prompt you used to describe the project to the AI for planning purposes
- a `PLAN.md` that generates the ABM implementation 
- ABM implementation code
- a `run_simulation.py` script that reproducibly runs the simulation and saves the results to a `results/` folder
- at least one context-management artifact used in this project (`SKILL.md` or `SUBAGENT.md`)
  - Make sure it is detailed enough to be useful. It should contain project-specific instructions, not just a copy of the assignment.
- a `Dockerfile` that reproduces the project environment.
- a `README.md` with three main sections:
  - **Model specification** describing agents, state variables, update rules, and metrics
  - **Results** summarizing the scientific conclusions (if any)
  - **Reflection** on how you ensured accuracy of the codebase, and whether you now trust the results.


The project should run with:

~~~bash
python run_simulation.py
~~~

## Submission

Submit a repository link that contains the `abm-project/` folder.

Throughout, you should always follow the techniques and practices we have covered in the course.