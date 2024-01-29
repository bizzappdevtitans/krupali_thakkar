from odoo import models, fields


class CourseDetails(models.Model):
    _name = "course.details"
    _description = "Details about the Course"
    _rec_name = "name"

    name = fields.Char(string="Name", help="Enter a course Name", required=True)
    student_ids = fields.One2many(
        "student.details", "course_field_id", string="Student Names", required=True
    )
    subject_ids = fields.One2many(
        "subject.details", "course_field_id", string="Subject Name"
    )
    teacher_ids = fields.One2many(
        "teachers.details", "course_field_id", string="Teacher Name"
    )
    exam_ids = fields.One2many("exam.details", "course_field_id", string="Exam Name")

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
                [("course_field_id", "=", self.name)]
            )

# count subjects
    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("course_field_id", "=", self.name)]
            )

# count teachers
    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("course_field_id", "=", self.name)]
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
                "domain": [("course_field_id", "=", self.name)],
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
                "domain": [("course_field_id", "=", self.name)],
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
                "domain": [("course_field_id", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }
