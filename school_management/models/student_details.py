from datetime import date
from odoo import models, fields, api


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Details about the students"
    _rec_name = "student_name"

    student_name = fields.Char("Student Name")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], "Gender")
    birth_date = fields.Date("Date Of birth")
    student_age = fields.Integer(string="Age", compute="_compute_age")
    father_name = fields.Char("Father Name")
    mother_name = fields.Char("Mother Name")
    student_phone = fields.Char("Phone Number")
    student_image = fields.Binary("Photo")
    student_email = fields.Char("Email")
    teacher_field_id = fields.Many2many(
        "teachers.details",
        "student_teacher_rel",
        "teacher_id",
        "student_id",
        "Teacher Name",
    )
    course_field_id = fields.Many2one("course.details", "course_name")
    subject_field_id = fields.Many2many(
        "subject.details",
        "subject_student_rel",
        "subject_id",
        "student_id",
        "Subject Name",
    )
    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")

    def _compute_age(self):
        for records in self:
            today = date.today()
            if records.birth_date:
                records.student_age = today.year - records.birth_date.year
            else:
                records.student_age = 0

    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("student_field_id", "=", self.student_name)]
            )

    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("student_field_id", "=", self.student_name)]
            )

    def action_view_teacher(self):
        return {
            "name": "Teachers",
            "res_model": "teachers.details",
            "view_mode": "tree,form",
            "context": {},
            "domain": [("student_field_id", "=", self.student_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def action_view_subjects(self):
        pass
