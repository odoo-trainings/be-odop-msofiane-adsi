from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # On the template, so every variant of a financeable model is financeable
    # too. product.product reads it through the template.
    is_financeable = fields.Boolean(string="Financeable")
