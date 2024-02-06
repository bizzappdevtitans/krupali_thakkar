from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_book = fields.Integer(string='Cancel Book',config_parameter="library_app_cancel_book")
