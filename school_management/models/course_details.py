from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class CourseDetails(models.Model):
    _name = "course.details"
    _description = "Details about the Course"
    _rec_name = "name"

    name = fields.Char(string="name", help="Enter a course Name", required=True)
    course_id = fields.Char(
        string="Course ID", required=True, index=True, copy=False, default="new"
    )
    start_date = fields.Date(string="start_date")
    end_date = fields.Date(string="end_date")
    student_ids = fields.One2many(
        comodel_name="student.details",
        inverse_name="course_ids",
        string="Student Names",
        required=True,
    )
    subject_ids = fields.One2many(
        comodel_name="subject.details", inverse_name="course_ids", string="Subject Name"
    )
    teacher_ids = fields.One2many(
        comodel_name="teachers.details",
        inverse_name="course_ids",
        string="Teacher Name",
    )
    book_ids = fields.One2many(
        comodel_name="library.details",
        inverse_name="course_id",
        string="Book Name",
    )
    exam_ids = fields.One2many(
        comodel_name="exam.details", inverse_name="course_ids", string="Exam Name"
    )

    student_count = fields.Integer(
        string="Students", compute="_compute_count_of_students"
    )
    subject_count = fields.Integer(
        string="Subjects", compute="_compute_count_of_subjects"
    )
    teachers_count = fields.Integer(
        string="Teachers", compute="_compute_count_of_teachers"
    )
    book_count = fields.Integer(string="Books", compute="_compute_count_of_books")

    # for unique course Name

    _sql_constraints = [
        (
            "unique_course",
            "unique(name)",
            "Course Name Must be unique",
        ),
    ]

    # count students
    def _compute_count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("course_ids", "=", self.name)]
            )

    # count subjects
    def _compute_count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("course_ids", "=", self.name)]
            )

    # count teachers
    def _compute_count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("course_ids", "=", self.name)]
            )

    # count books
    def _compute_count_of_books(self):
        for record in self:
            record.book_count = self.env["library.details"].search_count(
                [("course_id", "=", self.name)]
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

    # view book details

    def action_view_book(self):
        if self.book_count == 1:
            return {
                "name": "Books",
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "view_type": "form",
                "res_model": "library.details",
                "res_id": self.book_ids.id,
                "target": "new",
            }
        else:
            return {
                "name": "Books",
                "res_model": "library.details",
                "view_mode": "tree,form",
                "domain": [("course_id", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # sequence of student id

    @api.model
    def create(self, vals):
        vals["course_id"] = self.env["ir.sequence"].next_by_code("courseid.sequence")
        return super(CourseDetails, self).create(vals)

    # ORM name search method for search course name using multiple fields values

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("name", operator, name),
                ("course_id", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # get end date from system parameters

    @api.onchange("start_date")
    def get_end_date(self):
        months = self.env["ir.config_parameter"].get_param(
            "school_management_course_months"
        )
        self.end_date = self.start_date + relativedelta(months=int(months))
