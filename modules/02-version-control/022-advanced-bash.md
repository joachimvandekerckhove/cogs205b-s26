---
title: "Advanced bash"
course: COGS 205B
module: "02 — Version control"
---

# Advanced bash

- [Bash basics](./021-bash-basics.md) covered navigation, files, pipes, and redirection.  
- This chapter adds **superuser access**, **package management**, **search**, **aliases**, and **automation**.

---

# `sudo`

- **`sudo`** runs a single command with **root** (administrator) privileges.

```bash
sudo apt update
```

- In the class container the default user is often root already; on a shared machine you need `sudo`.

---

# Package management (APT)

- **`apt update`** — refresh the package index.  
- **`apt upgrade`** — upgrade installed packages.  
- **`apt install`** — install a new package.  
- **`apt remove`** — uninstall a package.

```bash
sudo apt update
sudo apt install ripgrep
sudo apt remove nano
```

- Update regularly for **security** patches on any Linux system.  
- Don't remove packages you do not recognize; many are **system dependencies**.

---

# Downloading files (`wget`)

- **`wget URL`** fetches a file over **HTTP/HTTPS** and saves it in the current directory (name taken from the URL unless you set **`-O path`**).

```bash
wget -O paper.pdf 'https://example.com/files/paper.pdf'
wget --quiet -O dataset.zip 'https://example.com/data/archive.zip'
```

- **`curl -L -o outfile URL`** is a common alternative (**`-L`** follows redirects). Install **`wget`** or **`curl`** in the container with **`apt`** if a minimal image lacks them, or add them to your Dockerfile.

---

# ZIP archives (`unzip`)

- **`unzip`** extracts **`.zip`** archives. Use **`-d dir`** to unpack into a directory (the directory is created if needed).

```bash
unzip -q archive.zip -d /tmp/my_extract
```

- **`-q`** is quiet. **`unzip -l archive.zip`** lists contents without extracting.

---

# Getting help

- **`man command`** — full manual page (`q` to quit).  
- **`command --help`** — quick summary.  
- **`man -k keyword`** — search manual pages by keyword.

```bash
man ls
ls --help
man -k copy
```

---

# Keyboard shortcuts

- **Tab** — auto-complete file names, commands, directories.  
- **Up / Down** — browse command history.  
- **Ctrl+R** — reverse-search through history.  
- **Ctrl+C** — stop a running command.

---

# Aliases

- An **alias** is a shortcut for a longer command.

```bash
alias ll='ls -alF'
alias please='sudo $(fc -ln -1)'
```

- **`alias`** (no arguments) lists current aliases.  
- **`unalias name`** removes one.  
- To keep aliases across sessions, add them to **`~/.bashrc`**:

```bash
echo "alias ll='ls -alF'" >> ~/.bashrc
source ~/.bashrc
```

---

# Searching text: `grep`

- **`grep`** finds lines matching a pattern.

```bash
grep 'error' /var/log/syslog
history | grep git
```

---

# Finding files

- **`find`** searches the filesystem by name, type, date, etc.

```bash
find . -name "*.txt"
find /workspace -type d -name "data"
```

- **`locate`** is faster (uses a pre-built index), but the index may be stale; update with `sudo updatedb`.

---

# Remote access: SSH and SCP

- **`ssh`** opens a shell on a remote machine.  
- **`scp`** copies files over SSH.

```bash
ssh user@hostname
scp results.csv user@hostname:/data/
```

- Key-based auth is covered in [SSH Keys](./024-ssh-keys.md).

---

# Scheduled tasks: `cron`

- **`crontab -e`** opens your personal cron table.  
- Each line: `minute hour day month weekday command`.

```bash
# Run backup every day at 5 AM
0 5 * * * /home/user/backup.sh
```

- **`crontab -l`** lists current jobs.

---

# Summary

- **`sudo`** for admin commands; **`apt`** for packages.  
- **`wget`** (or **`curl`**) to download files; **`unzip`** to extract **`.zip`** archives.  
- **`man`**, **`--help`**, **`man -k`** for documentation.  
- **Aliases** save keystrokes; put them in `~/.bashrc`.  
- **`grep`** and **`find`** to search text and files.  
- **`ssh`** / **`scp`** for remote work; **`cron`** for scheduled jobs.

---

[← Previous](021-bash-basics.md) · [Module 02](README.md) · [Course home](../../README.md) · [Next →](023-bash-scripting.md)
