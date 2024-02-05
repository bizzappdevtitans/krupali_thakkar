from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"
    cancel_days = fields.Integer(
        string="Cancel Days", config_parameter="school_management_cancel_days")
