# Assignment 2.09: documents
#
# One piece of paperwork attached to one loan application. This is the model
# behind the Compliance Checklist tab on the loan form.

from odoo import fields, models


class LoanApplicationDocument(models.Model):
    _name = "loan.application.document"
    _description = "Loan Application Document"

    name = fields.Char(string="Reference/Notes")

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="new",
        required=True,
    )

    type_id = fields.Many2one(
        comodel_name="loan.application.document.type",
        string="Document Type",
        required=True,
    )

    application_id = fields.Many2one(
        comodel_name="loan.application",
        string="Application",
        ondelete="cascade",
    )

    attachment_id = fields.Many2one(
        comodel_name="ir.attachment", string="File",
    )

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------

    # Assignment 3.03
    #
    # One action method per button in the inline checklist. write() rather
    # than self.state = ..., so they still work on several lines at once.
    def action_approve_document(self):
        self.write({"state": "approved"})

    def action_reject_document(self):
        self.write({"state": "rejected"})

    # ------------------------------------------------------------------
    # Submission rules
    # ------------------------------------------------------------------

    # Assignment 3.03
    #
    # The loan application asks each of its lines these two questions in
    # action_submit. They live on the document so the application never has
    # to know how a document makes up its mind, and the rules change in one
    # place. Both run on a single line.
    def _is_required_for_submit(self):
        """ Whether this line must be settled before its application can go out. """
        return self.type_id.is_required

    def _is_valid_for_submit(self):
        """ Whether this line is in a state the application can be submitted with. """
        return self.state == "approved"
