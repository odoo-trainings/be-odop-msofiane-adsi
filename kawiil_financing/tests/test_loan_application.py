# Assignment 3.06: the shipped test suite, run with
#     odoo-bin -u kawiil_financing --test-enable
#
# Each test covers something built in task 3: the arithmetic from 3.01, the
# constraints from 3.02, the submission guard from 3.03, the server action
# from 3.04 and the create() override from 3.05.
#
# test_06_sequence_number covers the reference sequence from 3.07.

import itertools

from odoo import Command
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, new_test_user


class TestLoanApplication(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # setUpClass runs once for the whole class, and everything it creates
        # is rolled back when the class finishes. Records made here are shared
        # by every test below and cost one round of database work; the same
        # code in setUp would run again before each test.
        cls.partner = cls.env["res.partner"].create({"name": "Test Rider"})
        cls.cosigner = cls.env["res.partner"].create({"name": "Test Co-Signer"})
        cls.other_user = new_test_user(cls.env, login="test_other_salesperson")
        cls.document_type = cls.env["loan.application.document.type"].create({
            "name": "Test Proof of Identity",
            "is_required": True,
        })
        cls._names = itertools.count(1)

    def _create_loan(self, **values):
        """ A valid application, with anything passed in overriding the
        defaults. Every call gets a reference of its own, since the unique
        constraint from 3.02 refuses two loans with the same one. """
        return self.env["loan.application"].create({
            "name": f"TEST/{next(self._names):03d}",
            "partner_id": self.partner.id,
            "principal_amount": 10000.0,
            "down_payment": 2000.0,
            "interest_rate": 7.5,
            **values,
        })

    def test_01_computes_and_crud(self):
        """ The loan amount is derived, and the checklist builds itself. """
        loan = self._create_loan()
        self.assertEqual(
            loan.loan_amount, 8000.0,
            "loan_amount should be the principal less the down payment",
        )
        self.assertTrue(
            loan.document_ids,
            "create() should have built a checklist from the document types",
        )

    def test_02_python_constraints(self):
        """ A down payment larger than the motorcycle is refused. """
        # Wrapping create() is enough: Odoo checks @api.constrains as part of
        # creating the record, so the error is raised before create() returns.
        with self.assertRaises(ValidationError):
            self._create_loan(principal_amount=5000.0, down_payment=10000.0)

    def test_03_cosigner_constraint(self):
        """ A customer cannot co-sign their own loan, whatever the form allows. """
        loan = self._create_loan(cosigner_ids=[Command.link(self.cosigner.id)])
        # The view domain from 2.03 would never offer this in the form. The
        # test goes around the form on purpose, which is exactly what an import
        # or a script would do.
        with self.assertRaises(ValidationError):
            loan.write({"cosigner_ids": [Command.link(self.partner.id)]})

    def test_04_assign_to_me(self):
        """ Assign to Me claims every selected loan at once. """
        loans = self._create_loan(user_id=self.other_user.id)
        loans |= self._create_loan(user_id=self.other_user.id)
        # Two records on purpose: the server action runs on the whole list
        # selection, and a method guarded with ensure_one() would fail here.
        loans.action_assign_to_me()
        self.assertEqual(loans.user_id, self.env.user)

    def test_05_workflow_user_error(self):
        """ An application whose checklist is unsettled cannot be submitted. """
        loan = self._create_loan()
        self.assertEqual(loan.state, "draft")
        # The lines create() added are still "new". Note which exception this
        # is: the constraints above raise ValidationError because they are
        # rules about the data, while this one raises UserError because it is
        # a rule about what somebody is allowed to do next.
        with self.assertRaises(UserError):
            loan.action_submit()

    # Assignment 3.07
    def test_06_sequence_number(self):
        """ A loan created without a reference gets one from the sequence. """
        # create() directly, _create_loan() always sets a name.
        loan = self.env["loan.application"].create({
            "partner_id": self.partner.id,
            "principal_amount": 10000.0,
            "down_payment": 2000.0,
            "interest_rate": 7.5,
        })
        self.assertTrue(loan.name)
        self.assertNotEqual(loan.name, self.env._("New"))
        self.assertTrue(
            loan.name.startswith("LOAN/"),
            "the reference should come from the loan.application sequence",
        )
