# Assignment 4.01: extension inheritance
#
# _inherit without _name adds to the existing res.partner instead of
# declaring a new model: no new table, and every other module's additions
# to contacts live side by side with these.
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # The reverse of loan.application.partner_id. Archived applications drop
    # out on their own, so it holds the live requests only.
    loan_application_ids = fields.One2many(
        comodel_name="loan.application",
        inverse_name="partner_id",
        string="Loan Applications",
    )
    # A different label from the One2many above, on purpose. Two fields on
    # one model sharing a label makes Odoo warn at startup, twice here since
    # res.users carries res.partner's fields too. Core does the same, e.g.
    # sale_order_count is "Sale Order Count".
    loan_application_count = fields.Integer(
        string="Loan Application Count",
        compute="_compute_loan_application_count",
    )

    @api.depends("loan_application_ids")
    def _compute_loan_application_count(self):
        for partner in self:
            partner.loan_application_count = len(partner.loan_application_ids)

    def action_view_loan_applications(self):
        # A window action opens one partner's list, and self.id on several
        # records would fail much further along.
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Loan Applications"),
            "res_model": "loan.application",
            "view_mode": "list,form",
            "domain": [("partner_id", "=", self.id)],
            # Pre-fills the customer when New is clicked from that list.
            "context": {"default_partner_id": self.id},
        }
