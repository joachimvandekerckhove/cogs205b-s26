# Homework (Module 02)

Complete this assignment inside the class Docker container using `git` and GitHub over SSH. Create a repository for this class if you do not have one yet. In your container, the repository should live at `/workspace/repo`.

On Canvas, submit the repository URL:
 
   `https://github.com/<your-username>/<repo-name>`

Your repository should contain the `scripts/` folder (with only the `fetch-csvs.sh` script defined below), the `data/` folder (with only the CSV files), and nothing else.

If you get stuck, _figure it out_.

---

# Product

Write a single bash script `./scripts/fetch-csvs.sh` that:

1. Downloads the ZIP file [data.zip](./files/data.zip) and unpacks it in a temporary directory.
2. Moves (or copies) only the CSV files (whose names end in `.csv`) that sit in the root of the unpacked archive (not inside subfolders) into a folder under your repository:

   `./data/<current-date>/`

   Use the calendar date `YYYY-MM-DD` as the folder name. Create the `data/` tree as needed.

3. Commits the CSV files under `data/` and itself to the repository, then pushes to GitHub.

