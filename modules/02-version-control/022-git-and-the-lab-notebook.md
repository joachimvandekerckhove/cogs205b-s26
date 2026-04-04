---
title: "Git and the lab notebook"
course: COGS 205B
module: "02 — Version control"
---

# Git and the lab notebook

- A **lab notebook** records what you tried, what worked, and what failed.  
- **Computational** work lives in **code**; a separate notebook duplicates that story.  
- **Version control** ties narrative to files: saves carry messages; you can **compare** and **roll back**.

---

# Git and hosting

- More than one version-control system exists; ***git*** is the norm in science and engineering.  
- **[GitHub](https://github.com)** (and similar hosts) provide storage, sharing, and review on top of git.

---

# In this module

- [SSH Keys](./021-ssh-keys.md)  
- [Branching and workflows](./023-version-control.md)  

---

# Why use the command line?

- GUIs for git are fine for many tasks.  
- The **CLI** behaves the same on a laptop, in a container, and on a cluster login node.  
- Everyone hits the same commands and error messages when asking for help.

---

# Discovering commands

- `git --help` lists subcommands.  
- `git <command> --help` documents one command in full.  
- Learn a **small** set by heart; use help and GUIs for the rest.

---

# What version control records

- An **annotated history** of every **tracked** file you commit.  
- Edits in your working tree are **not** history until you **commit**.  
- Each **commit** stores a snapshot plus metadata (time, author, parents, etc.).

---

# Tell git who you are

```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git config --global --list
```

- Run once per machine (or container). Commits are stamped with this identity.

---

# The usual loop

1. **Edit** files.  
2. **Stage** with `git add` (what enters the next snapshot).  
3. **Commit** with `git commit` and a message that states **why** the change matters.

---

# A practice folder

- Use an empty directory (e.g. under `/workspace` in the class container).

```bash
mkdir -p git-practice && cd git-practice
git init
echo "test file" > test_file.txt
git status
```

- **Untracked** files appear in `git status` until you add them.

---

# Stage changes

```bash
git add test_file.txt
git status
```

- Staging marks the file for the next commit; it is not yet permanent history.

---

# Make the first commit

```bash
git commit -m "initial add"
git status
```

- **Clean** working tree: files on disk match the latest commit.

---

# Commit hashes

- Every commit gets a unique **hash** (content + metadata).  
- Refer to commits by hash; the first several characters often suffice.  
- Hashes identify snapshots unambiguously when you merge, revert, or compare.

---

# Reading the log

```bash
git log
```

- Newest commits usually appear **first**.  
- Each line ties a **hash** to a **message**—your notebook entry for that step.

---

# History on GitHub and in the editor

- **Push** to GitHub to browse history in a web UI.  
- **VS Code** and **Cursor** expose **Source Control** for stage/commit/push flows.  
- CLI, web, and editor are views on the **same** commits.

---

# What changed? `git diff`

- Inspect unstaged edits before you add:

```bash
echo "another line" >> test_file.txt
git diff test_file.txt
```

- `+` **added** lines; `-` **removed** lines (in terminal colors when available).

---

# Save the next step

- Stage and commit when the diff matches **one** clear idea:

```bash
git add test_file.txt
git commit -m "add second line to test file"
git log
```

---

# Notebook vs. git history

- Paper: hard to **search**, easy to **lose**, handwriting fades.  
- Git: **searchable** log, **next to code**, each step tied to a **message**.  
- Answers **what**, **when**, and **why** without a parallel prose log.

---

# A commit-message shape

```text
<type>: <short summary>

<optional longer explanation>
```

- Typical **types**: `feature`, `bugfix`, `refactor`, `doc`, `test`, `cleanup`.  
- Keep the **first line** short (often under ~72 characters).

---

# Imperative mood and intent

- Write like a **command**: "add test for edge case," not "added test."  
- State **intent** and **problem solved**; the diff shows the code.  
- Future you reads `git log` more than the old notebook margin.

---

# One commit, one story

- One **coherent** change set per commit.  
- Avoid "everything from Tuesday" in a single commit.  
- Avoid splitting one logical fix across many commits that only make sense together.

---

# Staging on purpose

- `git add .` / `git add -A` grab **all** files in scope—often too much.  
- Risk: **secrets**, local config, unrelated edits; muddy messages; hard **reverts**.  
- Prefer `git add <path>…` explicitly.  
- `git add -u` updates **tracked** files only—still match the message.

---

# `.gitignore`

- Name patterns git should **never** track.  
- Typical entries: build artifacts, **`.venv`**, credentials, `__pycache__`, OS junk.  
- Keeps `git status` readable and avoids accidental leaks.

---

# Summary

- **Stage** deliberately; **commit** with **scoped**, **imperative** messages.  
- **`git log`** + **`git diff`** = searchable lab record beside the code.  
- Next: [Branching and workflows](./023-version-control.md) for branches, tags, and collaboration patterns.

---

# Further reading

- Russell A. Poldrack, *Better Code, Better Science* -- [book home](https://bettercodebetterscience.github.io/book/) (Essential tools and techniques, Version control).  
- [The curious coder's guide to git](https://matthew-brett.github.io/curious-git/index.html)  
- [Git tutorial](https://www.atlassian.com/git/tutorials/) · [Git cheat sheet (PDF)](../../img/git-cheat-sheet.pdf) · [Ubuntu CLI cheat sheet (PDF)](../../img/ubuntu-cli-cheat-sheet.pdf)

---

[← Previous](021-ssh-keys.md) · [Module 02](README.md) · [Course home](../../README.md) · [Next →](023-version-control.md)
