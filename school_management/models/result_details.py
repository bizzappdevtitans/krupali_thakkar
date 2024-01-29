from odoo import models, fields, api


class ResultDetails(models.Model):
    _name = "result.details"
    _description = "Details about the result"

    student_name = fields.Char("Student Name")
    student_id = fields.Integer("Student ID")
    student_course = fields.Char("Course")
    exam_name = fields.Many2many("exam.details", "exam")

    @api.onchange("student_id")
    def _view_student_name(self):
        view_student_id = self.env["student.details"].search(
            [("student_id", "=", self.student_id)]
        )

        self.student_name = view_student_id.student_name
        self.student_course = view_student_id.course_field_id.name
