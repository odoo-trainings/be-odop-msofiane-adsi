# Assignment 2.09: document types
#
# The kinds of paperwork a loan can require: proof of identity, proof of
# income, and so on. Configuration data, edited by admins and referenced by
# the documents themselves.

from odoo import fields, models


class LoanApplicationDocumentType(models.Model):
    _name = "loan.application.document.type"
    _description = "Loan Application Document Type"

    name = fields.Char(string="Document Name", required=True)

    is_required = fields.Boolean(string="Required")

    # active hides archived records instead of deleting them, so old documents
    # pointing at a retired type keep working.
    active = fields.Boolean(default=True)
