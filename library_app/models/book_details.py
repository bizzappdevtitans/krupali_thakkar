from odoo import fields, models, api
from odoo.exceptions import ValidationError


class BookDetails(models.Model):
    _name = "book.details"
    _description = "Information about book"
    _rec_name = "name"

    borrower_count = fields.Integer(
        string="count of borrower", compute="count_borrower"
    )

    name = fields.Char(string="name", help="Enter a Book Name", required=True)
    is_available = fields.Boolean(string="Is Available")
    book_type = fields.Selection(
        [
            ("paper", "Paperback"),
            ("hard", "Hardcover"),
            ("electronic", "Electronic"),
            ("other", "Other"),
        ],
        string="Type",
        help="select type of book",
    )
    number_of_books = fields.Integer(
        string="Number of book", help="Enter a number of books"
    )
    date_returned = fields.Date(string="Return Date")
    description = fields.Text(
        string="Description", help="Enter a description about book"
    )
    average_rating = fields.Float(
        string="Average Rating", help="Give a ratings to book"
    )
    date_published = fields.Date(
        string="Date of Publish", help="Enter a date of publish"
    )
    image = fields.Binary(string="Cover", help="Attach a book cover")
    last_borrow_date = fields.Datetime(
        string="Last Borrowed On", help="Enter a last borrow date"
    )
    active = fields.Boolean(default=True)
    rent_price = fields.Integer(string="Rent Price", help="Enter rent price of book")
    state = fields.Selection(
        [
            ("not_avalible", "Not Available"),
            ("available", "Available"),
        ],
        string="State",
    )
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    color = fields.Integer(string="Color")
    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Very High")],
        string="Priority",
    )

    borrower_ids = fields.Many2many(
        "borrower.details",
        "book_borrow_rel",
        "borrower_id",
        "book_id",
        string="Borrower Names",
    )

    tag_ids = fields.Many2many("book.tags", string="Tags")

    # check rent price
    @api.constrains("rent_price")
    def _check_rent_price(self):
        for records in self:
            if records.rent_price < 0:
                raise ValidationError("book price must be non zero positive number")

    # check numbers of books
    @api.constrains("number_of_books")
    def _check_number_of_books(self):
        for records in self:
            if records.number_of_books < 0:
                raise ValidationError("Number of books must not be zero Nagative")

    # set the state of the book
    @api.depends("state")
    def _compute_progress(self):
        for records in self:
            if records.state == "not_avalible":
                progress = 0
            elif records.state == "available":
                progress = 100
            else:
                progress = 0
            records.progress = progress

    # return book button
    @api.depends("number_of_books")
    def action_return(self):
        self.number_of_books += 1
        self.state = "available"

    # borrow book button
    @api.onchange("number_of_books")
    def action_borrow(self):
        self.number_of_books -= 1
        if self.number_of_books < 1:
            self.state = "not_avalible"

    # view borrower details

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

    # count borrowers

    def count_borrower(self):
        for records in self:
            records.borrower_count = len(self.borrower_ids)
