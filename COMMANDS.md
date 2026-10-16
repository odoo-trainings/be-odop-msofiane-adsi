# Command reference

Every command you need during the course, in one place. Replace anything in
`<angle brackets>` with your own value.

## Git workflow

Never commit to `production` directly. One branch per piece of work, then a
pull request.

```bash
# Tell git who you are, once per machine or new Odoo.sh container
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"

# Start a branch from an up-to-date production
git switch production
git pull
git switch -c 20.0-chapter-<n>-<your-github-username>

# Commit and push
git add <files>
git commit -m "[ADD] kawiil_financing: initialize the manifest"
git push -u origin 20.0-chapter-<n>-<your-github-username>
```

In the Odoo.sh web editor, `odoosh-push` pushes the branch you are on. Odoo.sh
needs a writable deploy key for that, set on the repository's Settings page.

Then open the pull request on GitHub, from your branch into `production`.

Commit messages follow `[TAG] module: what the change does`. The tag says what
kind of change it is: `ADD` for something new, `IMP` for an improvement to
something that already works, `FIX` for a bug fix, `REF` for a refactoring,
`REM` for a removal.

```bash
# Fix the last commit message before pushing
git commit --amend -m "[ADD] kawiil_financing: initialize the manifest"

# More work on a branch you already pushed
git add <files>
git commit -m "[FIX] kawiil_financing: correct the manifest category"
git push
```

## Running Odoo locally

Skip this section if you work entirely on Odoo.sh.

```bash
# Install the module into a database
odoo-bin -c <config-file> -d <database> -i kawiil_financing --stop-after-init

# Update it after you change Python or XML
odoo-bin -c <config-file> -d <database> -u kawiil_financing --stop-after-init

# Run its tests
odoo-bin -c <config-file> -d <database> -u kawiil_financing --test-enable --stop-after-init

# Start the server and leave it running
odoo-bin -c <config-file> -d <database>
```

`-i` installs, `-u` updates. You need `-u` after touching `__manifest__.py`,
adding a data file, or changing anything in `models/`: a restart alone is not
enough. `--stop-after-init` exits once the work is done instead of serving.

Demo data only loads into a database created with it enabled. Without it, the
records in `demo/` never appear, and neither does `base.res_partner_1`.

## The Odoo shell

A Python prompt with your database attached. This is how you inspect your work
before there is any user interface to click on.

```bash
odoo-bin shell -c <config-file> -d <database>
```

On Odoo.sh, open the branch Editor and start a new Shell from the launcher.

**Nothing you change here is saved.** The shell rolls the transaction back when
you exit. Run `env.cr.commit()` before leaving if you want a change to stick.
Reading and searching need no commit.

The shell runs as superuser, which is why you can read your model before it
has any access rules. A normal user cannot.

## ORM commands

`env` is your way into every model. `env["loan.application"]` is an empty
recordset you can search from.

```python
# Count and fetch
env["loan.application"].search_count([])
loans = env["loan.application"].search([])

# One field across every record in the set
loans.mapped("name")

# Follow a Many2one and read through it
loans.mapped("partner_id.name")

# Look a record up by the external id you gave it in XML
loan = env.ref("kawiil_financing.loan_application_demo_2")
loan.date_applied

# Filter in the database, with a domain
env["loan.application"].search([("state", "=", "sent")])
env["loan.application"].search([("loan_amount", ">", 10000)])

# Filter in Python, on records you already hold
loans.filtered(lambda loan: loan.loan_amount > 10000)
loans.sorted("date_applied")

# Read fields as dictionaries
loans.read(["name", "partner_id", "date_applied"])

# Modify
loan.write({"state": "approved"})
loan.state

# Create
new_loan = env["loan.application"].create({
    "name": "LOAN/SHELL/001",
    "partner_id": env.ref("base.res_partner_4").id,
    "interest_rate": 7.5,
    "loan_amount": 9500,
})

# Delete
new_loan.unlink()

# Keep your changes
env.cr.commit()
```

A domain is a list of `(field, operator, value)` tuples. An empty domain `[]`
matches everything. `search` filters in SQL and is what you want for anything
large; `filtered` filters records already in memory.

The create example matches the model as it stands in task 2. From 3.01 on,
`loan_amount` is computed: pass `principal_amount` instead.

## Code checks

The same checks the Quality Gate runs on your pull request. Run them before
you push and nothing will surprise you.

```bash
pip install -r requirements-dev.txt

ruff check --extend-exclude kawiil_base .
ruff check --extend-exclude kawiil_base . --fix   # fix what ruff can fix itself
```

pylint needs Odoo's own source next to it: Odoo's checkers ship inside it, and
one of them has to read Odoo's models to work.

```bash
PYTHONPATH=<odoo>:<odoo>/odoo/addons/test_lint/tests \
    pylint --rcfile=.pylintrc $(git ls-files '*.py')
```

`<odoo>` is the folder of your Odoo 20.0 checkout, the one holding `odoo-bin`.
