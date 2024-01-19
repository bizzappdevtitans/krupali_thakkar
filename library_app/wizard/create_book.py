from odoo import api, fields, models


class CreateBook(models.TransientModel):
    _name = "create.book.wizard"
    _description = "Create Book Wizard"

    name = fields.Char(string="Name", required=True)
    borrower_field_id = fields.Many2one("borrower.details",  "borrowername")

    def action_create_book(self):
        print("hello")
