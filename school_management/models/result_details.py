from odoo import models, fields, api


class ResultDetails(models.Model):
    _name = "result.details"
    _description = "Details about the result"

    student_name = fields.Char(string="Student Name")
    student_id = fields.Integer(
        string="Student ID", required=True, help="Enter student unique id"
    )
    student_course = fields.Char(string="Course")
    exam_name = fields.Many2many("exam.details", string="exam")

    # fetch student details from student ID

    @api.onchange("student_id")
    def _view_student_name(self):
        view_student_id = self.env["student.details"].search(
            [("student_id", "=", self.student_id)]
        )

        self.student_name = view_student_id.name
        self.student_course = view_student_id.course_ids.name
