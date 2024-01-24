from odoo import models, fields, api


class ResultDetails(models.Model):
    _name = "result.details"
    _description = "Details about the result"

    student_name = fields.Char("Student Name")
    student_id = fields.Integer("Student ID")
    student_course = fields.Char("Course")
    subject_name = fields.Many2many("subject.details", "subject")

    @api.onchange("student_id")
    def _view_student_name(self):
        student_field_id = self.env["student.details"].search(
            [("student_id", "=", self.student_id)]
        )

        self.student_name = student_field_id.student_name
        self.student_course = student_field_id.course_field_id.course_name
