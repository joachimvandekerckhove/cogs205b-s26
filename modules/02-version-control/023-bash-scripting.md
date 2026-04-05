---
title: "Bash scripting"
course: COGS 205B
module: "02 — Version control"
---

# Bash scripting

- A **script** is a text file of shell commands that runs as a single program.  
- Scripts turn multi-step terminal work into **repeatable**, **shareable** procedures.

---

# Creating and running a script

```bash
nano run_analysis.sh
```

```bash
#!/bin/bash
echo "Starting analysis..."
python src/analyze.py
echo "Done."
```

```bash
chmod +x run_analysis.sh
./run_analysis.sh
```

- **`#!/bin/bash`** (the shebang) tells the OS which interpreter to use.  
- **`chmod +x`** makes the file executable.

---

# Variables

```bash
NAME="experiment_01"
echo "Running $NAME"
echo "Output goes to output/${NAME}.csv"
```

- Assign with **no spaces** around `=`.  
- Reference with **`$VAR`** or **`${VAR}`** (braces clarify boundaries).

---

# Conditionals

```bash
if [ -f "data/raw.csv" ]; then
    echo "Raw data found."
elif [ -f "data/backup.csv" ]; then
    echo "Using backup."
else
    echo "No data available."
    exit 1
fi
```

- **`-f`** tests if a file exists; **`-d`** tests a directory.  
- **`exit 1`** signals failure to the caller.

---

# `for` loops

```bash
for file in data/*.csv; do
    echo "Processing $file"
    python src/clean.py "$file"
done
```

- Loops over every `.csv` in `data/`.  
- Quote `"$file"` to handle filenames with spaces.

---

# `while` loops

```bash
COUNT=1
while [ $COUNT -le 5 ]; do
    echo "Iteration $COUNT"
    ((COUNT++))
done
```

---

# Functions

```bash
greet() {
    echo "Hello, $1!"
}

greet "World"
greet "$USER"
```

- **`$1`**, **`$2`**, … are positional arguments to the function (or to the script when called from the command line).

---

# Useful built-ins

- **`read`** — prompt for user input.

```bash
echo "Enter subject ID:"
read SUBJECT
echo "Processing $SUBJECT"
```

- **`date`** — embed timestamps.

```bash
echo "Run started at $(date +%Y-%m-%d_%H:%M)"
```

- **`exit 0`** — end the script with success status.

---

# Debugging

- Run with **`bash -x script.sh`** to print each command before execution.  
- Inside a script, toggle with **`set -x`** / **`set +x`**:

```bash
set -x
python src/fit_model.py
set +x
```

---

# Comments

```bash
# This line is a comment
echo "This line runs"  # inline comment
```

---

# A small real-world script

```bash
#!/bin/bash
# preprocess.sh — clean raw data and produce summary
set -e   # stop on first error
RAW="data/raw"
OUT="data/processed"
mkdir -p "$OUT"
for csv in "$RAW"/*.csv; do
    base=$(basename "$csv")
    python src/clean.py "$csv" > "$OUT/$base"
done
echo "Cleaned $(ls "$OUT" | wc -l) files."
```

---

# Summary

- **Shebang** + **`chmod +x`** to create runnable scripts.  
- **Variables**, **conditionals** (`if`/`elif`/`else`), **loops** (`for`, `while`), **functions**.  
- **`set -e`** for fail-fast; **`bash -x`** for debugging.  
- Scripts turn one-off CLI steps into reproducible pipelines.

---

[← Previous](022-advanced-bash.md) · [Module 02](README.md) · [Course home](../../README.md) · [Next →](024-ssh-keys.md)
