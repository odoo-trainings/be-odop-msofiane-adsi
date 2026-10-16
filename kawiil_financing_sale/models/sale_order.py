from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    loan_application_ids = fields.One2many(
        comodel_name="loan.application",
        inverse_name="sale_order_id",
        string="Loan Applications",
    )
    # Its own label, a shared one makes Odoo warn at startup.
    loan_application_count = fields.Integer(
        string="Loan Application Count",
        compute="_compute_loan_application_count",
    )

    @api.depends("loan_application_ids")
    def _compute_loan_application_count(self):
        for order in self:
            order.loan_application_count = len(order.loan_application_ids)

    def action_create_loan(self):
        """ Open a new loan application pre-filled from this order. Nothing is
        saved until the user saves the form. """
        self.ensure_one()
        financeable_lines = self.order_line.filtered(
            lambda line: line.product_id.is_financeable,
        )
        if not financeable_lines:
            raise UserError(self.env._(
                "%s has no financeable product to start a loan for.",
                self.display_name,
            ))
        # One loan finances one vehicle.
        if len(financeable_lines) > 1:
            raise UserError(self.env._(
                "%s has several financeable products. A loan finances one, "
                "split the order first.",
                self.display_name,
            ))
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Loan Application"),
            "res_model": "loan.application",
            "view_mode": "form",
            "context": {
                "default_sale_order_id": self.id,
                "default_partner_id": self.partner_id.id,
                "default_product_id": financeable_lines.product_id.id,
                # A consumer loan finances what the customer pays for the
                # vehicle, tax included, in the order's currency.
                "default_principal_amount": financeable_lines.price_total,
                "default_currency_id": self.currency_id.id,
            },
        }

    def action_view_loan_applications(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Loan Applications"),
            "res_model": "loan.application",
            "view_mode": "list,form",
            "domain": [("sale_order_id", "=", self.id)],
            "context": {"default_sale_order_id": self.id},
        }
