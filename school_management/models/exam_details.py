from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Details about the exam"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter a exam name")
    exam_id = fields.Char(
        string="Exam ID", required=True, index=True, copy=False, default="new"
    )
    exam_date = fields.Date(string="Date Of Exam", help="enter date of exam")
    confirm_date = fields.Date(string="Confirm Date")
    duration = fields.Char(string="Duration")
    course_ids = fields.Many2one("course.details", string="Course Name", required=True)
    subject_ids = fields.Many2one(
        comodel_name="subject.details", string="Subject Name", required=True
    )
    student_ids = fields.Many2many(
        comodel_name="student.details",
        relation="exam_student_rel",
        column1="student_id",
        column2="exam_id",
        string="Student Name",
    )
    exam_type = fields.Char(string="exam Type")
    exam_marks = fields.Integer(string="Marks")

    student_count = fields.Integer(string="Students", compute="_count_of_students")

    # count of students

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("exam_ids", "=", self.name)]
            )

    # view student details

    def action_view_student(self):
        if self.student_count == 1:
            return {
                "name": "Students",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "student.details",
                "res_id": self.student_ids.id,
                "target": "new",
            }

        else:
            return {
                "name": "Students",
                "res_model": "student.details",
                "view_mode": "tree,form",
                "domain": [("exam_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # write type of exAM

    @api.onchange("duration")
    def write_exam_type(self):
        for records in self:
            if records.duration == "2 hours":
                records.write({"exam_type": "Intenal"})
            elif records.duration == "3 hours":
                records.write({"exam_type": "External"})
            else:
                records.write({"exam_type": None})

    # for geneating exam ids

    @api.model
    def create(self, vals):
        vals["exam_id"] = self.env["ir.sequence"].next_by_code("examid.sequence")
        return super(ExamDetails, self).create(vals)

    # ORM name get method for display name for many2many tags

    def name_get(self):
        res = []
        for records in self:
            res.append((records.id, "%s, %s" % (records.exam_id, records.name)))
        return res

    # ORM name search method for serch exam name using multiple field values

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("name", operator, name),
                ("duration", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

# get confirm date using system parameters

    @api.onchange("exam_date")
    def get_confirm_date(self):
        days = self.env["ir.config_parameter"].get_param(
            "school_management_cancel_days"
        )
        self.confirm_date = self.exam_date + relativedelta(days=int(days))
