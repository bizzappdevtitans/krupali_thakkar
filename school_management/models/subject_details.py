from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Details about the subjects"
    _rec_name = "subject_name"

    subject_name = fields.Char("Subject Name", required=True)
    course_field_id = fields.Many2one("course.details", "course_name", required=True)
    teacher_field_id = fields.Many2many(
        "teachers.details",
        "subject_teacher_rel",
        "teacher_id",
        "subject_id",
        "Teacher Name",
    )
    student_field_id = fields.Many2many(
        "student.details",
        "subject_student_rel",
        "student_id",
        "subject_id",
        "Student Name",
    )

    exam_field_id = fields.One2many("exam.details", "subject_field_id", "Exam Name")

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("subject_field_id", "=", self.subject_name)]
            )

    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("subject_field_id", "=", self.subject_name)]
            )

    def action_view_student(self):
        return {
            "name": "Students",
            "res_model": "student.details",
            "view_mode": "tree,form",
            "context": {},
            "domain": [("subject_field_id", "=", self.subject_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def action_view_teacher(self):
        return {
            "name": "Teachers",
            "res_model": "teachers.details",
            "view_mode": "tree,form",
            "context": {},
            "domain": [("subject_field_id", "=", self.subject_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    @api.constrains("subject_name")
    def _check_subject(self):
        for records in self:
            if records.subject_name == records.subject_name:
                raise ValidationError("Subject Name Must be unique")
