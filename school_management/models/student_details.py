from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Details about the students"
    _rec_name = "student_name"

    student_name = fields.Char("Student Name", required=True)
    student_id = fields.Integer("Student ID")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], "Gender", required=True
    )
    birth_date = fields.Date("Date Of birth")
    student_age = fields.Integer(string="Age", compute="_compute_age")
    father_name = fields.Char("Father Name")
    mother_name = fields.Char("Mother Name")
    student_phone = fields.Char("Phone Number")
    student_image = fields.Binary()
    student_email = fields.Char("Email")
    teacher_ids = fields.Many2many(
        "teachers.details",
        "student_teacher_rel",
        "teacher_id",
        "student_id",
        "Teacher Name",
    )
    course_field_id = fields.Many2one("course.details", "Course Name", required=True)
    subject_ids = fields.Many2many(
        "subject.details",
        "subject_student_rel",
        "subject_id",
        "student_id",
        "Subject Name",
    )
    exam_ids = fields.Many2many(
        "exam.details",
        "exam_student_rel",
        "exam_id",
        "student_id",
        "Exam Name",
    )
    reult_name = fields.One2many("result.details", "student_name", "result")

    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")
    exam_count = fields.Integer("Exams", compute="_count_of_exams")

    def _compute_age(self):
        for records in self:
            today = date.today()
            current_year = today.year

            if (
                records.birth_date.year > current_year - 100
                and records.birth_date.year < current_year - 10
            ):
                records.student_age = today.year - records.birth_date.year
            else:
                raise ValidationError("Enter valid birthdate")

    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("student_ids", "=", self.student_name)]
            )

    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("student_ids", "=", self.student_name)]
            )

    def _count_of_exams(self):
        for record in self:
            record.exam_count = self.env["exam.details"].search_count(
                [("student_ids", "=", self.student_name)]
            )

    _sql_constraints = [
        (
            "unique_student_id",
            "unique(student_id)",
            "Student id Must be unique",
        ),
    ]

    def action_view_teacher(self):
        if self.teachers_count == 1:
            return {
                "name": "Teachers",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "teachers.details",
                "res_id": self.teacher_ids.id,
                "target": "new",
            }
        else:
            return {
                "name": "Teachers",
                "res_model": "teachers.details",
                "view_mode": "tree,form",
                "context": {},
                "domain": [("student_ids", "=", self.student_name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    def action_view_subjects(self):
        if self.subject_count == 1:
            return {
                "name": "Subjects",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "subject.details",
                "res_id": self.subject_ids.id,
                "target": "new",
            }

        else:
            return {
                "name": "Subjects",
                "res_model": "subject.details",
                "view_mode": "tree,form",
                "context": {},
                "domain": [("student_ids", "=", self.student_name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    def action_view_exam(self):
        if self.exam_count == 1:
            return {
                "name": "Exams",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "exam.details",
                "res_id": self.exam_ids.id,
                "target": "new",
            }
        else:
            return {
                "name": "Exams",
                "res_model": "exam.details",
                "view_mode": "tree,form",
                "context": {},
                "domain": [("student_ids", "=", self.student_name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    def action_view_result(self):
        pass

    @api.onchange("student_phone")
    def validate_phone(self):
        if self.student_phone:
            match = re.match("^[0-9]\d{9}$", self.student_phone)
            if match == None:
                raise ValidationError("Enter Valid 10 digit Phone Number")

    @api.onchange("student_email")
    def validate_mail(self):
        if self.student_email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                self.student_email,
            )
            if match == None:
                raise ValidationError("Not a valid E-mail ID")
