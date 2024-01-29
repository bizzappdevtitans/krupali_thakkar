from odoo import models, fields


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Details about the exam"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    exam_date = fields.Date(string="Date Of Exam")
    duration = fields.Char(string="Duration")
    course_field_id = fields.Many2one("course.details", string="Course Name", required=True)
    subject_ids = fields.Many2one("subject.details", string="Subject Name", required=True)
    student_ids = fields.Many2many(
        "student.details",
        "exam_student_rel",
        "student_id",
        "exam_id",
        string="Student Name",
    )
    exam_marks = fields.Integer(string="Marks")

    student_count = fields.Integer(string="Students", compute="_count_of_students")

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("exam_ids", "=", self.name)]
            )

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
                "domain": [("exam_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }
