from odoo import models, fields


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Details about the exam"
    _rec_name = "exam_name"

    exam_name = fields.Char("Exam Name")
    exam_date = fields.Date("Date Of Exam")
    exam_duration = fields.Char("Duration")
    course_field_id = fields.Many2one("course.details", "Course Name", required=True)
    subject_field_id = fields.Many2one("subject.details", "Subject Name", required=True)
    student_field_id = fields.Many2many(
        "student.details",
        "exam_student_rel",
        "student_id",
        "exam_id",
        "Student Name",
    )

    student_count = fields.Integer("Students", compute="_count_of_students")

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("exam_field_id", "=", self.exam_name)]
            )

    def action_view_student(self):
        return {
            "name": "Students",
            "res_model": "student.details",
            "view_mode": "tree,form",
            "domain": [("exam_field_id", "=", self.exam_name)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
