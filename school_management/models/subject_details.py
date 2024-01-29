from odoo import models, fields


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Details about the subjects"
    _rec_name = "subject_name"

    subject_name = fields.Char("Subject Name", required=True)
    course_field_id = fields.Many2one("course.details", "course name", required=True)
    teacher_ids = fields.Many2many(
        "teachers.details",
        "subject_teacher_rel",
        "teacher_id",
        "subject_id",
        "Teacher Name",
    )
    student_ids = fields.Many2many(
        "student.details",
        "subject_student_rel",
        "student_id",
        "subject_id",
        "Student Name",
    )

    exam_ids = fields.One2many("exam.details", "subject_ids", "Exam Name")

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")

    _sql_constraints = [
        (
            "unique_subject",
            "unique(subject_name)",
            "Subject Name Must be unique",
        ),
    ]

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("subject_ids", "=", self.subject_name)]
            )

    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("subject_ids", "=", self.subject_name)]
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
                "context": {},
                "domain": [("subject_ids", "=", self.subject_name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

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
                "domain": [("subject_ids", "=", self.subject_name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }
