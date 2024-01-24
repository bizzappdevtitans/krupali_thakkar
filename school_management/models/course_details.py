from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CourseDetails(models.Model):
    _name = "course.details"
    _description = "Details about the Course"
    _rec_name = "course_name"

    course_name = fields.Char("Course Name")
    student_field_id = fields.One2many(
        "student.details", "course_field_id", "student_name"
    )
    subject_field_id = fields.One2many(
        "subject.details", "course_field_id", "subject_name"
    )
    teacher_field_id = fields.One2many(
        "teachers.details", "course_field_id", "teacher_name"
    )
    exam_field_id = fields.One2many("exam.details", "course_field_id", "Exam Name")

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")
    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")

    _sql_constraints = [
        (
            "unique_course",
            "unique(course_name)",
            "Course Name Must be unique",
        ),
    ]

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("course_field_id", "=", self.course_name)]
            )

    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("course_field_id", "=", self.course_name)]
            )

    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("course_field_id", "=", self.course_name)]
            )

    def action_view_student(self):
        return {
            "name": "Students",
            "res_model": "student.details",
            "view_mode": "tree,form",
            "domain": [("course_field_id", "=", self.course_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def action_view_subjects(self):
        return {
            "name": "Subjects",
            "res_model": "subject.details",
            "view_mode": "tree,form",
            "domain": [("course_field_id", "=", self.course_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }

    def action_view_teacher(self):
        return {
            "name": "Teachers",
            "res_model": "teachers.details",
            "view_mode": "tree,form",
            "domain": [("course_field_id", "=", self.course_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
