from odoo import fields, models


class BookTag(models.Model):
    _name = "book.tags"
    _description = "Tag of books"
    _rec_name = "tagname"

    tagname = fields.Char("Book Tag")
    tagcolor = fields.Integer("Tag color")

    book_ids = fields.Many2many("book.details", string="books")
