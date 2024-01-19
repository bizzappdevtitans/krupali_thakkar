from odoo import fields, models, api


class BookDetails(models.Model):
    _name = "book.details"
    _description = "Information about book"
    _rec_name = "bookname"

    borrower_count = fields.Integer(
        string="count of borrower", compute="count_borrower"
    )

    bookname = fields.Char("Bookname", required=True)
    is_available = fields.Boolean("Is Available")
    book_type = fields.Selection(
        [
            ("paper", "Paperback"),
            ("hard", "Hardcover"),
            ("electronic", "Electronic"),
            ("other", "Other"),
        ],
        "Type",
    )
    number_of_books = fields.Integer("Number of book")
    date_returned = fields.Date("Return Date")
    description = fields.Text("Description")
    average_rating = fields.Float("Average Rating", (3, 2))
    date_published = fields.Date()
    image = fields.Binary("Cover")
    last_borrow_date = fields.Datetime("Last Borrowed On")
    active = fields.Boolean(default=True)
    book_price = fields.Integer("Rent Price")
    state = fields.Selection(
        [
            ("not_avalible", "Not Available"),
            ("available", "Available"),
        ],
        "State",
    )
    progress = fields.Integer(string="Progress", compute="compute_progress")
    color = fields.Integer("Color")
    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Very High")], "Priority"
    )

    borrower_field_id = fields.Many2many(
        "borrower.details", "book_borrow_rel", "borrower_id", "book_id", "borrowername"
    )

    tag_ids = fields.Many2many("book.tags", string="Tags")

    _sql_constraints = [
        (
            "check_price",
            "check (book_price > 0)",
            "Rent must be non zero positive value ",
        ),
        (
            "check_count",
            "check (number_of_books >= 0)",
            "number must not be Nagative ",
        ),
    ]

    def action_confirm(self):
        print("button")

    @api.depends("state")
    def compute_progress(self):
        for records in self:
            if records.state == "not_avalible":
                progress = 0
            elif records.state == "available":
                progress = 100
            else:
                progress = 0
            records.progress = progress

    def action_return(self):
        self.number_of_books += 1
        self.state = "available"

    def action_borrow(self):
        self.number_of_books -= 1
        if self.number_of_books < 1:
            self.state = "not_avalible"

    def action_view_borrower(self):
        return {
            "name": ("Borrower"),
            "res_model": "borrower.details",
            "view_mode": "list,form",
            "context": {},
            "domain": [("book_field_id", "=", self.bookname)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def count_borrower(self):
        for records in self:
            records.borrower_count = len(self.borrower_field_id)
