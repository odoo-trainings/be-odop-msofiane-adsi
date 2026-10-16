# The loan.application model, built up across tasks 2, 3 and 4.
#
# Work through it one assignment at a time. Each section is tagged with the
# assignment that fills it in, and everything tagged with a later assignment
# stays commented out until you get there. The module has to install at every
# step, and code that refers to a field or model that does not exist yet stops
# the install.
#
# Lines starting with "# !" are changes a later assignment makes to code you
# have already written. Leave them exactly as they are, comment and all, until
# that assignment. Each one says which line it replaces.
#
# Nothing in this file loads until two imports are in place (assignment 2.02):
#   models/__init__.py            must import this file.
#   kawiil_financing/__init__.py  must import the models folder.

# Assignment 2.02
from odoo import fields, models

# ! Assignment 3.01 — leave this commented until you reach 3.01.
# ! The compute method needs the api decorators. It replaces the import line
# ! above; delete that one then.
# from odoo import api, fields, models

# ! Assignment 3.05 — leave this commented until you reach 3.05.
# ! Command joins the import. It replaces the 3.01 line above; delete that one
# ! then. Capitals sort first, which is the order ruff expects.
# from odoo import Command, api, fields, models

# ! Assignment 3.02 — leave this commented until you reach 3.02.
# from odoo.exceptions import ValidationError

# ! Assignment 3.03 — leave this commented until you reach 3.03.
# ! It replaces the 3.02 line above; delete that one then.
# from odoo.exceptions import UserError, ValidationError


class LoanApplication(models.Model):
    # The technical name of the model. Odoo derives the database table from it
    # by swapping dots for underscores, so this becomes loan_application. You
    # will use this string everywhere: in XML, in the ORM, and in the Models
    # list under Settings > Technical.
    _name = "loan.application"
    # A human-readable label. Odoo uses it in error messages and in the Models
    # list. Always set it, Odoo logs a warning if you don't.
    _description = "Loan Application"

    # ! Assignment 4.02 — leave this commented until you reach 4.02.
    # ! It goes alongside _name, it does not replace it.
    # _inherit = ["mail.thread", "mail.activity.mixin"]
    #
    # mail.thread brings the message history and followers, mail.activity.mixin
    # brings scheduled activities. Both are abstract models: they have no table
    # of their own, their fields and methods are folded into this model. With
    # _name kept, this model stays loan.application and gains what the mixins
    # define.

    # Assignment 2.02: the application's own data

    # Worked example. "string" is the label the user sees on screen. Leave it
    # off and Odoo derives one from the field name, which would give you "Name"
    # here rather than "Application Number".
    name = fields.Char(string="Application Number")

    # ! Assignment 2.08 — leave this commented until you reach 2.08.
    # ! It replaces the name line above; delete that one then.
    # name = fields.Char(string="Application Number", required=True)

    # ! Assignment 3.07 — leave this commented until you reach 3.07.
    # ! It replaces the 2.08 name line above; delete that one then.
    # ! "New" is a placeholder the create() override swaps for the next
    # ! sequence number. copy=False so a duplicate gets a number of its own
    # ! instead of clashing with the unique constraint.
    # name = fields.Char(
    #     string="Application Number",
    #     required=True,
    #     copy=False,
    #     default=lambda self: self.env._("New"),
    # )

    # TODO: loan_term — Integer, labelled "Term (Months)", defaulting to 36.

    # TODO: interest_rate — Float, labelled "Interest Rate", required=True.
    #       Pass digits=(5, 2) to store 5 digits in total with 2 of them after
    #       the decimal point.

    # TODO: date_applied — Date, labelled "Application Date", defaulting to
    #       today: default=fields.Date.context_today
    #
    #       Note there are no brackets and no lambda. A default takes the
    #       function itself and Odoo calls it per record. Use context_today
    #       rather than today: today gives the server's date, context_today
    #       gives the date in the user's own timezone, which is what someone
    #       filing an application late in the evening expects to see.

    # TODO: state — Selection offering, in this order: Draft, Sent, Approved,
    #       Rejected. The value is a list of (technical_key, label) tuples, the
    #       key is what gets stored, the label is what the user reads. Use the
    #       keys draft, sent, approved and rejected, and default to "draft".
    #       There is no cancelled state: abandoning an application means
    #       archiving it with the active field below.
    #
    #       Also pass copy=False. Duplicating an approved loan should give you
    #       a fresh draft to work from, not a second loan that claims to be
    #       approved. copy=False makes Odoo fall back to the default instead of
    #       carrying the value over.

    # ! Assignment 4.02 — leave your state field as it is until you reach 4.02.
    # ! Then add tracking=True to it. Every change to a tracked field is written
    # ! into the chatter by itself, old and new value side by side. Only state:
    # ! tracking every field turns the history into noise nobody reads.

    # TODO: active — Boolean defaulting to True. Odoo treats this exact field
    #       name specially: setting it to False hides the record from list
    #       views instead of deleting it, which is how archiving works.

    # TODO: notes — Html, labelled "Internal Notes", copy=False. Notes are
    #       about one specific application, so they should not follow a
    #       duplicate to the new record.

    # Assignment 2.03: links to the rest of Odoo

    # Worked example. Uncomment it when you reach 2.03. A Many2one holds a link
    # to one record in another model. comodel_name says which model, and Odoo
    # stores the other record's database id in a partner_id column.
    # partner_id = fields.Many2one(
    #     comodel_name="res.partner", string="Customer", required=True,
    # )

    # TODO: user_id — Many2one to "res.users", labelled "Salesperson",
    #       defaulting to whoever is logged in. self.env.user is the current
    #       user, so: default=lambda self: self.env.user

    # TODO: product_id — Many2one to "product.product", labelled "Motorcycle".
    #       product.product is the variant, the record that actually gets sold
    #       and stocked. product.template is the abstract product above it.

    # TODO: currency_id — Many2one to "res.currency". A Monetary field cannot
    #       format an amount without knowing its currency, so give this one a
    #       default rather than leaving it empty:
    #       default=lambda self: self.env.company.currency_id

    # TODO: loan_amount — Monetary, required=True, with
    #       currency_field="currency_id".

    # ! Assignment 3.01 — leave this commented until you reach 3.01.
    # ! It replaces your loan_amount field; delete that one then.
    # ! loan_amount is no longer typed in, it is worked out from the principal
    # ! and the down payment, so required moves to principal_amount (3.01,
    # ! below). store=True keeps a column behind it, so it can still be
    # ! searched, sorted and grouped on.
    # loan_amount = fields.Monetary(
    #     compute="_compute_loan_amount",
    #     inverse="_inverse_loan_amount",
    #     store=True,
    #     currency_field="currency_id",
    # )

    # TODO: down_payment — Monetary, with currency_field="currency_id".
    #
    #       Monetary is a Float that Odoo renders with a currency symbol and
    #       the right number of decimals. The field named in currency_field
    #       has to exist on this same model, which is why currency_id comes
    #       first.

    # TODO: cosigner_ids — Many2many to "res.partner", labelled "Co-Signers".
    #       A loan can have any number of guarantors next to the customer. Add
    #       domain="[('id', '!=', partner_id)]" so the customer is not offered
    #       as their own co-signer. That domain only filters the dropdown in
    #       the form; 3.02 adds the rule that holds everywhere else.
    #
    #       partner_id and cosigner_ids both point at res.partner. Odoo tells
    #       the two apart because one is a single link and the other a set,
    #       each with its own column or join table.

    # Assignment 2.09: categorisation and compliance

    # Worked example. Uncomment it when you reach 2.09, once the tag model next
    # door exists. A Many2many links this record to many tags, and each tag back
    # to many loans. Odoo creates the join table that makes that work; you never
    # touch it.
    # tag_ids = fields.Many2many(comodel_name="loan.application.tag", string="Tags")

    # TODO: document_ids — One2many to "loan.application.document", labelled
    #       "Compliance Documents". A One2many is not stored: it is the mirror
    #       image of a Many2one on the other model, so it has to be told which
    #       field over there points back here. That is
    #       inverse_name="application_id".

    # Assignment 3.01: related and computed fields

    # Worked example. Uncomment it when you reach 3.01. A related field reads
    # through a link: this one shows the customer's email on the application.
    # Leave the defaults alone, read-only and not stored, the value always comes
    # from the contact itself.
    # email = fields.Char(related="partner_id.email")

    # TODO: phone — the same, related to the customer's phone.

    # TODO: principal_amount — Monetary, labelled "Principal Amount",
    #       required=True, currency_field="currency_id". The full price of the
    #       motorcycle, and the figure the user types in now that loan_amount
    #       is worked out from it.

    # Assignment 3.03: workflow dates

    # Worked example. Uncomment it when you reach 3.03. No default: the action
    # methods stamp it when the decision is actually taken, not when the record
    # is created.
    # date_approved = fields.Date(string="Approval Date")

    # TODO: date_rejected — Date, labelled "Rejection Date", same idea.

    # Assignment 3.02: database constraints
    #
    # A models.Constraint is a class attribute holding the SQL and the message
    # shown when it is violated. PostgreSQL enforces it, so it holds however
    # the record was made: the form, an import, or the shell.
    #
    # Worked example. Uncomment it when you reach 3.02.
    # _name_uniq = models.Constraint(
    #     "UNIQUE(name)",
    #     "Two applications cannot share the same reference.",
    # )
    #
    # TODO: _principal_check, following the example above: a CHECK that keeps
    #       principal_amount strictly above zero. Nobody finances a motorcycle
    #       that costs nothing.

    # ------------------------------------------------------------------
    # Compute and inverse methods
    # ------------------------------------------------------------------

    # Assignment 3.01
    #
    # The two methods behind loan_amount. Their names are the strings you pass
    # to compute= and inverse= on the field.
    #
    # Uncomment both when you reach 3.01. The decorator matters: leave it off
    # and the field is computed once and never refreshed.
    #
    # @api.depends("principal_amount", "down_payment")
    # def _compute_loan_amount(self):
    #     # TODO: the arithmetic is right, the shape is wrong. This assigns to
    #     #       self, which only works when self holds exactly one record. A
    #     #       compute method is handed every record that needs the value at
    #     #       once, so as soon as two applications are read together it fails
    #     #       with:
    #     #
    #     #           ValueError: Expected singleton: loan.application(1, 2, 3)
    #     #
    #     #       That is the error you will meet most often in Odoo, and it
    #     #       always means code written for one record was given several.
    #     #       Wrap the line in `for application in self:` and assign to
    #     #       application instead of self.
    #     self.loan_amount = self.principal_amount - self.down_payment
    #
    # def _inverse_loan_amount(self):
    #     # TODO: the same arithmetic rearranged, in the shape you just gave the
    #     #       compute. Odoo calls this on save for the records whose
    #     #       loan_amount was typed in by hand, and principal_amount is the
    #     #       figure that stays put:
    #     #           down_payment = principal_amount - loan_amount
    #     pass

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------

    # Assignment 3.02
    #
    # Python constraints, for rules SQL is the wrong tool for. @api.constrains
    # re-runs the method whenever one of the listed fields is written. Unlike
    # the SQL constraints above, it only fires on writes that go through
    # the ORM, and it can say exactly what went wrong.
    #
    # Uncomment when you reach 3.02.
    #
    # @api.constrains("principal_amount", "down_payment")
    # def _check_down_payment(self):
    #     # TODO: loop over self, and raise ValidationError where down_payment
    #     #       is greater than or equal to principal_amount. Wrap the message
    #     #       in self.env._("...") so it can be translated.
    #     pass
    #
    # TODO: _check_cosigner_ids, decorated with
    #       @api.constrains("partner_id", "cosigner_ids"). Raise
    #       ValidationError where a loan's partner_id is among its own
    #       cosigner_ids: a customer cannot co-sign their own loan. The domain
    #       from 2.03 only stops this in the form, this stops it in imports,
    #       scripts and the shell too.

    # ------------------------------------------------------------------
    # CRUD overrides
    # ------------------------------------------------------------------

    # Assignment 3.05
    #
    # The compliance checklist should build itself: nobody should have to add
    # a line by hand for every document the dealership always asks for.
    #
    # Two methods, kept apart on purpose: a helper that decides which document
    # types belong on a new application, and a create() override that turns
    # them into lines. Split that way, a module extending this one can change
    # what lands on the checklist by overriding the helper alone.
    #
    # The helper is written for you. @api.model because it runs before any
    # record exists, so there is no recordset for it to work on. Uncomment it
    # when you reach 3.05.
    #
    # @api.model
    # def _get_default_document_types(self):
    #     """ The document types that belong on a new application's checklist. """
    #     # search([]) already leaves out archived types: the model has an
    #     # active field, and Odoo filters on it unless told otherwise.
    #     return self.env["loan.application.document.type"].search([])
    #
    # TODO: the override itself. It is not stubbed on purpose: a create() that
    #       forgets to return super()'s result breaks every record creation in
    #       the module, demo data included, so write it whole:
    #
    #           @api.model_create_multi
    #           def create(self, vals_list):
    #               ...
    #               return super().create(vals_list)
    #
    #       In between, for each vals dict in vals_list, turn each document type
    #       into a line with Command.create({"type_id": doc_type.id}) and put
    #       the list in vals["document_ids"]. Use
    #       vals.get("document_ids", []) + commands so lines somebody already
    #       filled in during creation survive.
    #
    #       Command.create(...) is the named form of the tuple (0, 0, {...})
    #       you met in 2.09. Both work, Command is easier to read.

    # ! Assignment 3.07 — leave this until you reach 3.07.
    # ! Then add this to the loop in your create(), before super() is called.
    # ! A new application arrives with the "New" placeholder, or no name at
    # ! all, and leaves with the next number from the sequence:
    # !
    # !     if vals.get("name", self.env._("New")) == self.env._("New"):
    # !         vals["name"] = self.env["ir.sequence"].next_by_code(
    # !             "loan.application"
    # !         ) or self.env._("New")

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------

    # Assignment 3.03
    #
    # The three buttons in the form header call these methods by name. A
    # method behind a type="object" button takes no arguments beyond self, and
    # what it returns goes back to the web client. Returning nothing reloads
    # the record, which is all a transition needs.
    #
    # action_approve_loan is the worked example. The other two follow its
    # shape: loop over self, skip any record that is not in the state the
    # transition starts from, then write the change. Uncomment all three when
    # you reach 3.03.
    #
    # def action_approve_loan(self):
    #     for loan in self:
    #         if loan.state != "sent":
    #             continue
    #         # Both values in one write, on purpose. Users may only change
    #         # applications that are not approved yet (security/ir.access.csv),
    #         # so a second write after the state is already "approved" would
    #         # be refused for them. Testing as an admin hides this.
    #         loan.write({
    #             "state": "approved",
    #             "date_approved": fields.Date.context_today(loan),
    #         })
    #
    # def action_reject_loan(self):
    #     # TODO: state to "rejected", date_rejected to today. Same shape as
    #     #       action_approve_loan, including the single write.
    #     pass
    #
    # def action_submit(self):
    #     # TODO: the check first, the state change second.
    #     #
    #     #       Ask each document line whether it counts, rather than reaching
    #     #       into its type from here. The document already knows:
    #     #
    #     #           required_docs = loan.document_ids.filtered(
    #     #               lambda doc: doc._is_required_for_submit()
    #     #           )
    #     #
    #     #       Raise a UserError if there are none at all, and again if any of
    #     #       them fails _is_valid_for_submit(). Wrap both messages in
    #     #       self.env._(). It takes arguments too, so
    #     #       self.env._("Document %s is not approved.", doc.display_name)
    #     #       stays translatable. Never build the sentence with an f-string:
    #     #       the translation export would see a different string each time.
    #     #
    #     #       Only once that passes: state to "sent", date_applied to today.
    #     #
    #     # ! Assignment 4.02 — leave this commented until you reach 4.02.
    #     # ! Then post a note straight after the state changes, inside the loop:
    #     # !
    #     # !     loan.message_post(
    #     # !         body=self.env._("Application submitted for review."),
    #     # !         subtype_xmlid="mail.mt_note",
    #     # !     )
    #     # !
    #     # ! On loan, not self: message_post writes to one record. mail.mt_note
    #     # ! is the internal note subtype, so it lands in the history without
    #     # ! emailing the followers.
    #     pass

    # Assignment 3.04
    #
    # The method behind the "Assign to Me" server action. Unlike the three
    # above, it has no business looking at one record at a time: the server
    # action hands it the whole selection from the list view, and one write
    # updates all of them. No ensure_one() either, a selection of several
    # records is exactly what it is for.
    #
    # Uncomment it when you reach 3.04.
    #
    # def action_assign_to_me(self):
    #     # TODO: write the current user (self.env.user) into user_id on every
    #     #       record in self, with a single self.write({...}).
    #     pass
