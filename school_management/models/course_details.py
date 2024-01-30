from odoo import models, fields, api


class CourseDetails(models.Model):
    _name = "course.details"
    _description = "Details about the Course"
    _rec_name = "name"

    name = fields.Char(string="Name", help="Enter a course Name", required=True)
    course_id = fields.Char(
        string="Course ID", required=True, index=True, copy=False, default="new"
    )
    student_ids = fields.One2many(
        "student.details", "course_ids", string="Student Names", required=True
    )
    subject_ids = fields.One2many(
        "subject.details", "course_ids", string="Subject Name"
    )
    teacher_ids = fields.One2many(
        "teachers.details", "course_ids", string="Teacher Name"
    )
    exam_ids = fields.One2many("exam.details", "course_ids", string="Exam Name")

    student_count = fields.Integer(string="Students", compute="_count_of_students")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")
    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")

    # for unique course Name

    _sql_constraints = [
        (
            "unique_course",
            "unique(name)",
            "Course Name Must be unique",
        ),
    ]

    # count students
    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("course_ids", "=", self.name)]
            )

    # count subjects
    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("course_ids", "=", self.name)]
            )

    # count teachers
    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("course_ids", "=", self.name)]
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
                "domain": [("course_ids", "=", self.name)],
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
                "domain": [("course_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # view teachers details

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
                "domain": [("course_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # sequence of course id

    @api.model
    def create(self, vals):
        vals["course_id"] = self.env["ir.sequence"].next_by_code("courseid.sequence")
        return super(CourseDetails, self).create(vals)
