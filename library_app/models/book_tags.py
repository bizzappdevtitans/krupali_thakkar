from odoo import fields, models


class BookTag(models.Model):
    _name = "book.tags"
    _description = "Tag of books"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter a Tag")
    color = fields.Integer(string="Color", help="Enter a tag color")

    book_ids = fields.Many2many("book.details", string="books")

    book_count = fields.Integer(string="count of book", compute="count_book")
    # for unique tag
    _sql_constraints = [("unique_tag_name", "unique (name)", "Tag must be unique")]

    # count the books
    def count_book(self):
        for records in self:
            records.book_count = len(self.book_ids)

    # book view

    def action_view_book(self):
        return {
            "name": ("Books"),
            "res_model": "book.details",
            "view_mode": "tree,form",
            "context": {},
            "domain": [("tag_ids", "=", self.name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
