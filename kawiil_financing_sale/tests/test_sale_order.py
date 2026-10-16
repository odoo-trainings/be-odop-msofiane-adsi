# Assignment 4.03: the provided test suite for the sales bridge.
#
# You are not asked to change anything in this file. Build the module until
# every test passes:
#     odoo-bin -u kawiil_financing_sale --test-enable
#
# Read the tests as the specification. Each one names the fields and methods
# it expects, and the assertion messages say what was wrong when one fails.
# The two UI requirements, the "Create Loan" header button and the smart
# button, are not covered here: check those by hand in the browser.

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.sale.tests.common import SaleCommon


# post_install: sale orders lean on accounting setup that is only complete once
# every module is installed, so these run after installation, like sale's own.
@tagged("post_install", "-at_install")
class TestSaleOrderLoan(SaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # SaleCommon brings a customer (cls.partner) and two products that are
        # not financeable (cls.product, cls.service_product), with taxes
        # switched off. The motorcycle gets a sales tax of its own, so the
        # amounts with and without tax differ.
        cls.sales_tax = cls.env["account.tax"].create({"name": "Test Sales Tax 10%", "amount": 10})
        cls.motorcycle, cls.scooter = cls.env["product.product"].create([
            {
                "name": "Test Motorcycle",
                "list_price": 12000.0,
                "is_financeable": True,
                "taxes_id": [Command.set(cls.sales_tax.ids)],
            },
            {"name": "Test Scooter", "list_price": 3000.0, "is_financeable": True},
        ])

    def _confirmed_order(self, *products):
        """ A confirmed sale order with one line per product given. """
        order = self._create_so(order_line=[
            Command.create({"product_id": product.id}) for product in products
        ])
        order.action_confirm()
        return order

    def test_01_data_model(self):
        """ The three fields the bridge adds exist, with the right shape. """
        is_financeable = self.env["product.template"]._fields.get("is_financeable")
        self.assertTrue(is_financeable, "product.template needs an is_financeable field")
        self.assertEqual(is_financeable.type, "boolean")

        sale_order_id = self.env["loan.application"]._fields.get("sale_order_id")
        self.assertTrue(sale_order_id, "loan.application needs a sale_order_id field")
        self.assertEqual(sale_order_id.type, "many2one")
        self.assertEqual(sale_order_id.comodel_name, "sale.order")

        loan_application_ids = self.env["sale.order"]._fields.get("loan_application_ids")
        self.assertTrue(loan_application_ids, "sale.order needs a loan_application_ids field")
        self.assertEqual(loan_application_ids.type, "one2many")
        self.assertEqual(loan_application_ids.comodel_name, "loan.application")
        self.assertEqual(
            loan_application_ids.inverse_name, "sale_order_id",
            "loan_application_ids should be the other side of loan.application.sale_order_id",
        )

    def test_02_no_financeable_product(self):
        """ An order with nothing to finance cannot start a loan. """
        order = self._confirmed_order(self.product)
        with self.assertRaises(UserError):
            order.action_create_loan()

    def test_03_several_financeable_products(self):
        """ One loan finances one vehicle, so two financeable lines are refused. """
        order = self._confirmed_order(self.motorcycle, self.scooter)
        with self.assertRaises(UserError):
            order.action_create_loan()

    def test_04_create_loan_action(self):
        """ The action opens a new loan pre-filled from the order. """
        order = self._confirmed_order(self.motorcycle, self.product)
        motorcycle_line = order.order_line.filtered(lambda line: line.product_id == self.motorcycle)

        action = order.action_create_loan()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "loan.application")
        context = action["context"]
        self.assertEqual(context["default_sale_order_id"], order.id)
        self.assertEqual(context["default_partner_id"], order.partner_id.id)
        self.assertEqual(
            context["default_product_id"], self.motorcycle.id,
            "the loan should be for the financeable product, not the other line",
        )
        # A consumer loan finances what the customer actually pays for the
        # vehicle, tax included.
        self.assertNotEqual(motorcycle_line.price_total, motorcycle_line.price_subtotal)
        self.assertEqual(
            context["default_principal_amount"], motorcycle_line.price_total,
            "the principal should be the vehicle line's total, tax included",
        )

    def test_05_loan_links_back_to_order(self):
        """ A loan saved from the action shows up on the order it came from. """
        order = self._confirmed_order(self.motorcycle)
        action = order.action_create_loan()

        # What the form does when the user saves: create a record with the
        # action's context, so every default_ key fills its field.
        loan = self.env["loan.application"].with_context(**action["context"]).create({
            "interest_rate": 6.5,
        })

        self.assertEqual(loan.sale_order_id, order)
        self.assertEqual(loan.partner_id, order.partner_id)
        self.assertEqual(order.loan_application_ids, loan)
        self.assertEqual(
            order.loan_application_count, 1,
            "the smart button counts the loans linked to the order",
        )
