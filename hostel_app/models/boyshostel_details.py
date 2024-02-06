from odoo import fields, models


class BoysHostelDetails(models.Model):
    _name = "boyshostel.details"
    _description = "Information about the hostel"

    name = fields.Char()
