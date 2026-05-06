# Homework — Video walkthrough of Module 4 Bayes-factor code

## Purpose

Practice explaining real software clearly and tying implementation plus tests to **clean-code concerns** (code smells and refactoring ideas). You will walk another competent programmer through what you submitted for Module 4.

Use your **Module 4 homework submission**: `bayes_factor/bayes_factor.py` and `bayes_factor/tests/test_bayes_factor.py` from your repository as they stood when you submitted them (the video should match that submission).

---

## Deliverable

Submit a **single prerecorded video of 9-10 minutes**.

- Record **screen capture + voice** so viewers can follow code on screen while you speak.
- Submit the video to the Canvas assignment as a .mkv or .mp4 file.
- At the start of the recording, please say your name.

---

## Part 1 — Implementation (`bayes_factor.py`)

Goal: explain your implementation **line by line** (or small contiguous blocks if two lines form one idea), **as if briefing a busy technical manager** who wants to trust that you understand every choice.  If multiple segments are very similar, you can skip duplicates.

For each segment you should cover:

- **What** the line or block does.
- **Why** it is written that way (alternatives you rejected are welcome if brief).
- Any **code smells** that apply to the line or block.
- Any **refactorings** you could apply (what you would extract, rename, or simplify).

Code is _never perfect_ -- every implementation has code smells and potential refactorings.  

If you run short on time, you can skip lines/segments so you can focus on the most important code smells and refactorings.

---

## Part 2 — Test suite (`tests/test_bayes_factor.py`)

Goal: walk through the tests **one test method at a time** (in file order unless you explain a different order).

For **each** `test_*` method:

- State in plain language **what behavior or contract** it checks.
- Point out **which assertions** implement that check.

Then emphasize anything you did **that wasn't discussed in the Module 4 lecture**.

You do **not** need to explain basics already emphasized in Module 4 slides (for example plain `assertEqual` on integers or a bare `assertRaises` without regex), except briefly when they appear inside a larger test.

---

## Constraints

- Stay within **10 minutes** total.
- The video must be **your own explanation** of **your own** Module 4 submission.
- You may show a terminal briefly (for example how you run tests), but most time should be on the **implementation and tests**.


## Protip for recording presentations

Do everything in one take, but speak clearly and deliberately with a short pause between segments. That way you can delete segments to trim the video to the desired length. If you feel you messed up a segment, start over without stopping the recording. I use [ShotCut](https://www.shotcut.org/) to edit my videos, but [OBS](https://obsproject.com/) is also very good and [YouTube Studio](https://www.youtube.com/studio) is convenient if you don't mind uploading to the cloud.

---

## Reading

- Module 5 chapters on code smells and refactoring (especially vocabulary for Part 1).
- Module 4 homework specification for context: [Bayes factor test suite](../04-test-driven-development/homework.md).

[Module 05](README.md) · [Course home](../../README.md)
