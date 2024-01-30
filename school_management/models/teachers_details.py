from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TeachersDetails(models.Model):
    _name = "teachers.details"
    _description = "Information about the teachers"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter teacher name")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender", required=True
    )
    phone_number = fields.Char(string="Contact Number", required=True)
    email = fields.Char(string="Email ID", required=True)
    course_ids = fields.Many2one("course.details", string="course name", required=True)
    subject_ids = fields.Many2many(
        "subject.details",
        "subject_teacher_rel",
        "subject_id",
        "teacher_id",
        string="Subject Name",
    )
    student_ids = fields.Many2many(
        "student.details",
        "student_teacher_rel",
        "student_id",
        "teacher_id",
        string="Student Name",
    )

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")
    experiance = fields.Integer(string="Experiance in years")

    # count of students

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("teacher_ids", "=", self.name)]
            )

    # count of subjects

    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("teacher_ids", "=", self.name)]
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
                "context": {},
                "domain": [("teacher_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # view subject details

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
                "domain": [("teacher_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # phone number validation

    @api.onchange("phone_number")
    def validate_phone(self):
        if self.phone_number:
            match = re.match("^[0-9]\d{9}$", self.phone_number)
            if match == None:
                raise ValidationError("Enter Valid 10 digit Phone Number")

    # email validation

    @api.onchange("email")
    def validate_mail(self):
        if self.email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                self.email,
            )
            if match == None:
                raise ValidationError("Not a valid E-mail ID")
