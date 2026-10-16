# Assignment 4.01: extension inheritance
#
# Drop the noqa once you have uncommented the block below and all three
# names are in use.
from odoo import api, fields, models  # noqa: F401

# TODO: write the class declaration. It is the only part of this file you type
# yourself, because it is the whole mechanism:
#
#     class ResPartner(models.Model):
#         _inherit = "res.partner"
#
# _inherit on its own, with no _name, means "do not declare a new model, add
# to the one that already exists". No table is created and no data is copied.
# Everything in the class lands on res.partner itself, next to what base and
# every other installed module put there. That is why a dozen modules can each
# add fields to a contact without any of them knowing about the others.
#
# Add _name as well and you get something different: a new model that copies
# res.partner's definition and goes its own way. Here you want extension.
#
# Then uncomment the block below into it. It is indented to sit inside the
# class, so it drops straight in once your two lines are above it. Read it as
# you go, the comments in it are the point of the assignment:
#
#   loan_application_ids            the reverse of loan.application.partner_id.
#                                   Archived applications drop out on their
#                                   own, so it holds the live requests only.
#   loan_application_count          what the smart button displays.
#   action_view_loan_applications   what the smart button calls.

#     loan_application_ids = fields.One2many(
#         comodel_name="loan.application",
#         inverse_name="partner_id",
#         string="Loan Applications",
#     )
#
#     # A different label from the One2many above, on purpose. Two fields on
#     # one model sharing a label makes Odoo warn at startup, and it warns twice
#     # here: res.users carries res.partner's fields too, so the clash is
#     # reported against both models. Core names these the same way, e.g.
#     # sale_order_count is "Sale Order Count".
#     loan_application_count = fields.Integer(
#         string="Loan Application Count",
#         compute="_compute_loan_application_count",
#     )
#
#     @api.depends("loan_application_ids")
#     def _compute_loan_application_count(self):
#         for partner in self:
#             partner.loan_application_count = len(partner.loan_application_ids)
#
#     def action_view_loan_applications(self):
#         # ensure_one() because a window action can only open one partner's
#         # list, and self.id on several records fails much further along.
#         self.ensure_one()
#         return {
#             "type": "ir.actions.act_window",
#             "name": self.env._("Loan Applications"),
#             "res_model": "loan.application",
#             "view_mode": "list,form",
#             "domain": [("partner_id", "=", self.id)],
#             # default_partner_id is how Odoo pre-fills a field on a new
#             # record: click New from the list this opens and the customer is
#             # already set.
#             "context": {"default_partner_id": self.id},
#         }
