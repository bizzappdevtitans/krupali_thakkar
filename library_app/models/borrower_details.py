from odoo import fields, models


class BorrowerDetails(models.Model):
    _name = "borrower.details"
    _description = "details of borrower"
    _rec_name = "borrowername"

    borrowername = fields.Char("BorrowerName")

    book_field_id = fields.One2many("book.details", "borrower_field_id", "bookname")
