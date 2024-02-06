from odoo import api, fields, models


class ActivityDetails(models.Model):
    _name = "activity.details"
    _description = "Details about Activities"
    _rec_name = "name"

    activity_id = fields.Char(
        string="Activity ID", required=True, copy=False, index=True, default="new"
    )
    name = fields.Char(string="name")
    fees = fields.Integer(string="Activity Fees")
    student_ids = fields.Many2many(
        comodel_name="student.details",
        relation="student_activity_rel",
        column1="student_id",
        column2="activity_id",
        string="Students",
    )
    color = fields.Integer("color")

    @api.model
    def create(self, vals):
        vals["activity_id"] = self.env["ir.sequence"].next_by_code(
            "activityid.sequence"
        )
        return super(ActivityDetails, self).create(vals)

    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("name", operator, name),
                ("activity_id", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    def name_get(self):
        res = []
        for records in self:
            res.append((records.id, "%s,%s" % (records.activity_id, records.name)))
        return res
