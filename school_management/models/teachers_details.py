from odoo import models, fields


class TeachersDetails(models.Model):
    _name = "teachers.details"
    _description = "Information about the teachers"
    _rec_name = "teacher_name"

    teacher_name = fields.Char("Teacher Name")
    teacher_gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], "Gender"
    )
    teacher_phone_number = fields.Integer("Contact Number")
    teacher_email = fields.Char("Email ID")
    course_field_id = fields.Many2one("course.details", "course_name", required=True)
    subject_field_id = fields.Many2many(
        "subject.details",
        "subject_teacher_rel",
        "subject_id",
        "teacher_id",
        "Subject Name",
    )
    student_field_id = fields.Many2many(
        "student.details",
        "student_teacher_rel",
        "student_id",
        "teacher_id",
        "Student Name",
    )

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")
    experiance = fields.Integer("Experiance")

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("teacher_field_id", "=", self.teacher_name)]
            )

    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("teacher_field_id", "=", self.teacher_name)]
            )

    def action_view_student(self):
        return {
            "name": "Students",
            "res_model": "student.details",
            "view_mode": "tree,form",
            "context": {},
            "domain": [("teacher_field_id", "=", self.teacher_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def action_view_subjects(self):
        return {
            "name": "Subects",
            "res_model": "subject.details",
            "view_mode": "tree,form",
            "context": {},
            "domain": [("teacher_field_id", "=", self.teacher_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
