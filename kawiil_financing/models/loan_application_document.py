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
    # One action method per button in the inline checklist. A type="object"
    # button calls the method on the line it sits on. write() rather than
    # self.state = ..., so the same method still works if it is ever called on
    # several lines at once.
    #
    # Worked example. Uncomment it when you reach 3.03.
    #
    # def action_approve_document(self):
    #     self.write({"state": "approved"})
    #
    # TODO: action_reject_document, the other half of the pair. Same shape,
    #       with the state it belongs to. The button you add for it in the
    #       form is wired by this exact name.

    # ------------------------------------------------------------------
    # Submission rules
    # ------------------------------------------------------------------

    # Assignment 3.03
    #
    # The loan application asks each of its lines these two questions when
    # someone tries to submit it. They live here, on the document, rather than
    # on the application: the application never has to know how a document
    # makes up its mind, and when the rules change they change in one place.
    # You call both from action_submit.
    #
    # Both run on one line at a time, so self is a single record. Uncomment
    # them when you reach 3.03, they are written for you.
    #
    # def _is_required_for_submit(self):
    #     """ Whether this line must be settled before its application can go out. """
    #     return self.type_id.is_required
    #
    # def _is_valid_for_submit(self):
    #     """ Whether this line is in a state the application can be submitted with. """
    #     return self.state == "approved"
