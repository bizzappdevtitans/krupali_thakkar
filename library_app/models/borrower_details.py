from odoo import fields, models


class BorrowerDetails(models.Model):
    _name = "borrower.details"
    _description = "details of borrower"
    _rec_name = "borrowername"

    borrowername = fields.Char("BorrowerName")

    book_count = fields.Integer(string="count of book", compute="count_book")

    book_field_id = fields.One2many("book.details", "borrower_field_id", "bookname")

    def action_view_book(self):
        return {
            "name": ("Books"),
            "res_model": "book.details",
            "view_mode": "list,form",
            "context": {},
            "domain": [("borrower_field_id", "=", self.borrowername)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def count_book(self):
        for records in self:
            records.book_count = len(self.book_field_id)
