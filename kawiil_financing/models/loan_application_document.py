# Assignment 2.09: documents
#
# One piece of paperwork attached to one loan application. This is the model
# behind the Compliance Checklist tab you add to the loan form.
#
# Follow the pattern in loan_application_tag.py.

# fields is unused until you write your first field below, which makes the
# Quality Gate flag it as an unused import. noqa silences that one check on
# this one line. Delete the comment once you have added a field.
from odoo import fields, models  # noqa: F401


class LoanApplicationDocument(models.Model):
    _name = "loan.application.document"
    _description = "Loan Application Document"

    # TODO: name — Char, labelled "Reference/Notes".

    # TODO: state — Selection with keys new, approved and rejected, labelled
    #       New, Approved and Rejected, string "Status". Default to "new" and
    #       make it required.

    # TODO: type_id — Many2one to "loan.application.document.type", labelled
    #       "Document Type", required=True. A line without a type has nothing
    #       to check against.

    # TODO: application_id — Many2one to "loan.application", labelled
    #       "Application". This is the field document_ids on the loan points
    #       back through, so the two have to agree: name it exactly this or the
    #       One2many will not resolve. Add ondelete="cascade": a checklist line
    #       means nothing once its loan is deleted.

    # TODO: attachment_id — Many2one to "ir.attachment", labelled "File".
    #       ir.attachment is Odoo's own model for stored files, so you get
    #       upload and download for free instead of building it.

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
