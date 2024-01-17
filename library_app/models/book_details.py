from odoo import fields, models, api


class BookDetails(models.Model):
    _name = "book.details"
    _description = "Information about book"
    _rec_name = "bookname"

    book_count = fields.Integer(compute="count")

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
    date_returned = fields.Date("Return Date")
    description = fields.Text("Description")
    average_rating = fields.Float("Average Rating", (3, 2))
    date_published = fields.Date()
    image = fields.Binary("Cover")
    last_borrow_date = fields.Datetime("Last Borrowed On")
    active = fields.Boolean(default=True)
    book_price = fields.Char("Rent Price")
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

    borrower_field_id = fields.Many2one("borrower.details", "borrowername")

    tag_ids = fields.Many2many("book.tags", string="Tags")

    def action_confirm(self):
        print("button")

    @api.depends("state")
    def compute_progress(self):
        for records in self:
            if records.state == "not_avalible":
                progress = 0
            elif records.state == "borrowed":
                progress = 50
            elif records.state == "available":
                progress = 100
            elif records.state == "return":
                progress = 100
            else:
                progress = 0
            records.progress = progress

    @api.depends()
    def count(self):
        count = self.env["book.details"].search_count([("is_available", "=", "True")])
        self.book_count = count

    def action_return(self):
        self.state = "available"

    def action_borrow(self):
        self.state = "not_avalible"
