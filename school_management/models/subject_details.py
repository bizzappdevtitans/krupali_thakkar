from odoo import models, fields, api
from odoo.exceptions import UserError


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Details about the subjects"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter subject name")
    subject_id = fields.Char(
        string="Subject ID", required=True, index=True, copy=True, default="new"
    )
    course_ids = fields.Many2one("course.details", string="course name", required=True)
    teacher_ids = fields.Many2many(
        "teachers.details",
        "subject_teacher_rel",
        "teacher_id",
        "subject_id",
        string="Teacher Name",
    )
    student_ids = fields.Many2many(
        "student.details",
        "subject_student_rel",
        "student_id",
        "subject_id",
        string="Student Name",
    )

    color = fields.Integer()

    exam_ids = fields.One2many("exam.details", "subject_ids", string="Exam Name")

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")

    # set subject name as unique

    _sql_constraints = [
        (
            "unique_subject",
            "unique(name)",
            "Subject Name Must be unique",
        ),
    ]

    # count of students

    def _count_of_students(self):
        for record in self:
            students = self.env["student.details"].search(
                [("subject_ids", "=", self.name)]
            )
            record.student_count = len(students)

    # count of teachers

    def _count_of_teachers(self):
        for record in self:
            teachers = self.env["teachers.details"].search_read(
                [("subject_ids", "=", self.name)]
            )
            record.teachers_count = len(teachers)

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
                "domain": [("subject_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # view teacher details

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
                "domain": [("subject_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # create subject id

    @api.model
    def create(self, vals):
        vals["subject_id"] = self.env["ir.sequence"].next_by_code("subjectid.sequence")
        return super(SubjectDetails, self).create(vals)

    def unlink(self):
        for record in self:
            if record.student_ids:
                raise UserError(("You cannot Delete this record"))
        return super(SubjectDetails, self).unlink()
