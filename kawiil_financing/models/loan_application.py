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

# Assignment 2.02, api added by 3.01, Command by 3.05
from odoo import Command, api, fields, models

# Assignment 3.02, UserError added by 3.03
from odoo.exceptions import UserError, ValidationError


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

    # Without string, Odoo would label this field "Name". Assignment 2.08
    # made it required, 3.07 gave it the "New" placeholder that create()
    # swaps for the next sequence number. copy=False so a duplicate gets a
    # number of its own instead of clashing with the unique constraint.
    name = fields.Char(
        string="Application Number",
        required=True,
        copy=False,
        default=lambda self: self.env._("New"),
    )

    loan_term = fields.Integer(string="Term (Months)", default=36)
    interest_rate = fields.Float(
        string="Interest Rate", required=True, digits=(5, 2),
    )
    # context_today, not today: the date in the user's timezone rather than
    # the server's. Passed uncalled, so Odoo evaluates it per record.
    date_applied = fields.Date(
        string="Application Date", default=fields.Date.context_today,
    )
    # No cancelled state: an abandoned application is archived instead.
    # copy=False so a duplicate starts again as a draft.
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        default="draft",
        copy=False,
    )

    # ! Assignment 4.02 — leave your state field as it is until you reach 4.02.
    # ! Then add tracking=True to it. Every change to a tracked field is written
    # ! into the chatter by itself, old and new value side by side. Only state:
    # ! tracking every field turns the history into noise nobody reads.

    active = fields.Boolean(default=True)
    # Notes are about this application only, a duplicate should not get them.
    notes = fields.Html(string="Internal Notes", copy=False)

    # Assignment 2.03: links to the rest of Odoo

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )
    # The variant, the record that is actually sold, not the template above it.
    product_id = fields.Many2one(
        comodel_name="product.product", string="Motorcycle",
    )
    # Monetary fields need a currency to format their amounts.
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id,
    )
    # Assignment 3.01 made it computed from the principal and the down
    # payment. store=True keeps a column, so it can still be searched, sorted
    # and grouped on.
    loan_amount = fields.Monetary(
        compute="_compute_loan_amount",
        inverse="_inverse_loan_amount",
        store=True,
        currency_field="currency_id",
    )

    down_payment = fields.Monetary(currency_field="currency_id")
    # The domain only filters the dropdown, _check_cosigner_ids enforces it
    # everywhere.
    cosigner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Co-Signers",
        domain="[('id', '!=', partner_id)]",
    )

    # Assignment 2.09: categorisation and compliance

    # Odoo creates and manages the join table behind a Many2many.
    tag_ids = fields.Many2many(comodel_name="loan.application.tag", string="Tags")
    # Not stored: the mirror of application_id on the document model.
    document_ids = fields.One2many(
        comodel_name="loan.application.document",
        inverse_name="application_id",
        string="Compliance Documents",
    )

    # Assignment 3.01: related and computed fields

    # Read-only and not stored, so the value always comes from the contact.
    email = fields.Char(related="partner_id.email")
    phone = fields.Char(related="partner_id.phone")
    # The full price of the motorcycle, the figure the user types in.
    principal_amount = fields.Monetary(
        string="Principal Amount", required=True, currency_field="currency_id",
    )

    # Assignment 3.03: workflow dates

    # No default: the action methods stamp the date when the decision is
    # actually taken, not when the record is created.
    date_approved = fields.Date(string="Approval Date")
    date_rejected = fields.Date(string="Rejection Date")

    # Assignment 3.02: database constraints
    #
    # PostgreSQL enforces these, so they hold however the record was made:
    # the form, an import, or the shell.
    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "Two applications cannot share the same reference.",
    )
    _principal_check = models.Constraint(
        "CHECK(principal_amount > 0)",
        "The principal amount must be above zero.",
    )

    # ------------------------------------------------------------------
    # Compute and inverse methods
    # ------------------------------------------------------------------

    # Assignment 3.01
    #
    # A compute method gets every record that needs the value at once, so it
    # loops: assigning to self only works for a single record.
    @api.depends("principal_amount", "down_payment")
    def _compute_loan_amount(self):
        for application in self:
            application.loan_amount = (
                application.principal_amount - application.down_payment
            )

    # Called on save when loan_amount was typed in by hand. The principal is
    # the figure that stays put, the down payment absorbs the difference.
    def _inverse_loan_amount(self):
        for application in self:
            application.down_payment = (
                application.principal_amount - application.loan_amount
            )

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------

    # Assignment 3.02
    #
    # Python constraints, for rules SQL is the wrong tool for. They only fire
    # on writes that go through the ORM, but they can say exactly what went
    # wrong.
    @api.constrains("principal_amount", "down_payment")
    def _check_down_payment(self):
        for application in self:
            if application.down_payment >= application.principal_amount:
                raise ValidationError(self.env._(
                    "The down payment must be lower than the principal amount.",
                ))

    # The domain on cosigner_ids only filters the form, this also covers
    # imports, scripts and the shell.
    @api.constrains("partner_id", "cosigner_ids")
    def _check_cosigner_ids(self):
        for application in self:
            if application.partner_id in application.cosigner_ids:
                raise ValidationError(self.env._(
                    "A customer cannot co-sign their own loan.",
                ))

    # ------------------------------------------------------------------
    # CRUD overrides
    # ------------------------------------------------------------------

    # Assignment 3.05
    #
    # The compliance checklist builds itself. A helper decides which document
    # types belong on a new application and create() turns them into lines,
    # so a module extending this one can change the checklist by overriding
    # the helper alone.

    # @api.model: it runs before any record exists, so there is no recordset
    # for it to work on.
    @api.model
    def _get_default_document_types(self):
        """ The document types that belong on a new application's checklist. """
        # search([]) already leaves out archived types: the model has an
        # active field, and Odoo filters on it unless told otherwise.
        return self.env["loan.application.document.type"].search([])

    @api.model_create_multi
    def create(self, vals_list):
        doc_types = self._get_default_document_types()
        for vals in vals_list:
            # Assignment 3.07: a new application arrives with the "New"
            # placeholder, or no name at all, and leaves with the next number.
            if vals.get("name", self.env._("New")) == self.env._("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "loan.application",
                ) or self.env._("New")
            # Appended, so lines somebody filled in during creation survive.
            vals["document_ids"] = vals.get("document_ids", []) + [
                Command.create({"type_id": doc_type.id}) for doc_type in doc_types
            ]
        return super().create(vals_list)

    # ------------------------------------------------------------------
    # Action methods
    # ------------------------------------------------------------------

    # Assignment 3.03
    #
    # The three buttons in the form header call these methods by name. Each
    # one skips records that are not in the state its transition starts
    # from. Returning nothing reloads the record, which is all a transition
    # needs.
    def action_approve_loan(self):
        for loan in self:
            if loan.state != "sent":
                continue
            # Both values in one write, on purpose. Users may only change
            # applications that are not approved yet (security/ir.access.csv),
            # so a second write after the state is already "approved" would
            # be refused for them. Testing as an admin hides this.
            loan.write({
                "state": "approved",
                "date_approved": fields.Date.context_today(loan),
            })

    def action_reject_loan(self):
        for loan in self:
            if loan.state != "sent":
                continue
            loan.write({
                "state": "rejected",
                "date_rejected": fields.Date.context_today(loan),
            })

    def action_submit(self):
        for loan in self:
            if loan.state != "draft":
                continue
            # Each line decides whether it counts, the loan does not reach
            # into document types itself.
            required_docs = loan.document_ids.filtered(
                lambda doc: doc._is_required_for_submit(),
            )
            if not required_docs:
                raise UserError(self.env._(
                    "Add the required documents before submitting %s.",
                    loan.display_name,
                ))
            for doc in required_docs:
                if not doc._is_valid_for_submit():
                    # Arguments, never an f-string, so the message stays one
                    # translatable string.
                    raise UserError(self.env._(
                        "Document %s is not approved.", doc.display_name,
                    ))
            loan.write({
                "state": "sent",
                "date_applied": fields.Date.context_today(loan),
            })
            # ! Assignment 4.02 — leave this commented until you reach 4.02.
            # ! Then post a note straight after the state changes, inside the
            # ! loop:
            # !
            # !     loan.message_post(
            # !         body=self.env._("Application submitted for review."),
            # !         subtype_xmlid="mail.mt_note",
            # !     )
            # !
            # ! On loan, not self: message_post writes to one record.
            # ! mail.mt_note is the internal note subtype, so it lands in the
            # ! history without emailing the followers.

    # Assignment 3.04
    #
    # The method behind the "Assign to Me" server action. The action hands it
    # the whole list selection and one write updates all of it. No
    # ensure_one(): several records is exactly what it is for.
    def action_assign_to_me(self):
        self.write({"user_id": self.env.user.id})
