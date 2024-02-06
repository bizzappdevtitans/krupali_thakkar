from odoo import models, fields


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"
    cancel_days = fields.Integer(
        string="Cancel Days", config_parameter="school_management_cancel_days"
    )

    return_days = fields.Integer(
        string="Return Days", config_parameter="school_management_book_return_days"
    )

    course_months = fields.Integer(
        string="course_months", config_parameter="school_management_course_months"
    )
