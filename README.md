# Odoo Developer Onboarding Program (ODOP)

This is your assignment repository for the K'awiil Motors course. It holds the
starting structure of the modules you will build, and the automated checks that
run on every pull request you open.

The course tasks tell you what to build. This file explains how the repository
works.

## Getting started

1. Accept the invitation to your private repository (task 1.01).
2. Deploy your Odoo.sh project and link it to this repository (task 1.02).
3. Pick a local setup or the Odoo.sh web editor (task 1.03).

`COMMANDS.md` lists every command you will need: git, Odoo, the shell and the
code checks. Keep it open.

## Working in branches

Never commit to `production` directly. Each task gets its own branch, and
reaches `production` through a pull request.

- Branch names follow `20.0-chapter-<n>-<your-github-username>`, where `<n>`
  is the task number, for example `20.0-chapter-2-jdoe`. The autograder reads
  the chapter from the branch name, so a branch without it is not graded.
- Commit messages follow Odoo's format, `[TAG] module: what the change does`,
  for example `[ADD] kawiil_financing: add loan.application model`. Each
  assignment gives you the exact message.
- Each task ends with a closing pull request into `production` (1.05, 2.10,
  3.08, 4.04).

## The Quality Gate

Every pull request into `production` runs the checks in
`.github/workflows/quality-gate.yml`:

- the autograder, which checks your work against the requirements of the task
  in the branch name and posts the result as a comment on the pull request.
  From task 1.04 on, that includes `kawiil_base` as a submodule at
  `odoo-trainings/kawiil_base`;
- `ruff check`, with the same configuration Odoo uses on its own code;
- `pylint`, limited to the checks Odoo runs on its own code, such as SQL
  injection and untranslated error messages.

Your tests run on Odoo.sh, in the build of your branch.

If a check fails, open "Details" on the pull request, fix the problem, and push
again. The checks run again on their own. Your instructor reviews a pull
request once it passes.

## What is in the repository

- `kawiil_financing/`: the module you build in tasks 2 to 4. Its files are
  already in place, waiting for you to fill them in.
- `kawiil_financing_sale/tests/`: the test suite for task 4.03. The module
  around it is yours to create.
- `.github/`, `.pylintrc`, `ruff.toml`, `requirements-dev.txt`: the Quality Gate
  and the tools it uses. Do not edit them.
- `COMMANDS.md`: the command reference.

## How to read the starter code

The files contain the scaffolding for every assignment at once, so most of
what you open belongs to work you have not reached yet. Everything for a later
assignment is commented out, because the module has to install at every step:
uncommenting a link to a field or model that does not exist yet breaks the
install.

- `# Assignment 2.03` marks where an assignment's work starts.
- A **worked example** is code written for you. Uncomment it when you reach
  its assignment: remove the comment markers and nothing else.
- A **TODO** is code you write yourself. The comment says what the field or
  method needs and anything non-obvious about it.
- Lines starting with **`# !`** are changes a later assignment makes to code you
  have already written. Leave them exactly as they are until that assignment.
  Each one says which line it replaces.

The same rule applies to `__manifest__.py`. The `data` and `demo` lists show
every file you will register, each tagged with the assignment that adds it. Add
each line when you reach that assignment, in the position shown: Odoo reads the
files in order, and a file can only refer to what the files above it created.

## Solutions

The branches `20.0-solution-chapter-2`, `-3` and `-4` hold the finished code
for each task, one commit per assignment. Use them to compare your work once
you have tried an assignment yourself, and build one on Odoo.sh when you want
to see the expected result running.
