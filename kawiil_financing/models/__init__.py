# Import each model file so Odoo loads it: one relative import per file, with
# no .py extension. Nothing in this folder is loaded until it is imported here,
# and this file in turn does nothing until kawiil_financing/__init__.py
# imports the folder.
#
# Uncomment each line in the assignment that creates the file, not before:
# importing a file that does not exist yet stops the whole module from loading.

from . import (
    # Assignment 2.02: the main model.
    loan_application,
    # Assignment 2.09: tags, document types and the compliance checklist.
    loan_application_document,
    loan_application_document_type,
    loan_application_tag,
)

# Assignment 4.01: the extension of res.partner.
# from . import res_partner
