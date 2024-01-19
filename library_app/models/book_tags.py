from odoo import fields, models


class BookTag(models.Model):
    _name = "book.tags"
    _description = "Tag of books"
    _rec_name = "tagname"

    tagname = fields.Char("Book Tag")
    tagcolor = fields.Integer("Tag color")

    book_ids = fields.Many2many("book.details", string="books")

    book_count = fields.Integer(string="count of book", compute="count_book")

    _sql_constraints = [
        ("unique_tag_name", "unique (tagname)", "BookTag must be unique")
    ]

    def count_book(self):
        for records in self:
            records.book_count = len(self.book_ids)

    def action_view_book(self):
        return {
            "name": ("Books"),
            "res_model": "book.details",
            "view_mode": "list,form",
            "context": {},
            "domain": [("tag_ids", "=", self.tagname)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
