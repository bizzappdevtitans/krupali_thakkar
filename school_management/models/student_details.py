from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import re


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Details about the students"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter student name")
    student_id = fields.Char(
        string="student ID", required=True, index=True, copy=False, default="new"
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender", required=True
    )
    birth_date = fields.Date(string="Date Of birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    father_name = fields.Char(string="Father Name")
    mother_name = fields.Char(string="Mother Name")
    phone_number = fields.Char(string="Phone Number")
    image = fields.Binary()
    email = fields.Char(string="Email")
    teacher_ids = fields.Many2many(
        comodel_name="teachers.details",
        relation="student_teacher_rel",
        column1="teacher_id",
        column2="student_id",
        string="Teacher Name",
    )
    course_ids = fields.Many2one(
        comodel_name="course.details", string="Course Name", required=True
    )
    subject_ids = fields.Many2many(
        comodel_name="subject.details",
        relation="subject_student_rel",
        column1="subject_id",
        column2="student_id",
        string="Subject Name",
    )
    exam_ids = fields.Many2many(
        comodel_name="exam.details",
        relation="exam_student_rel",
        column1="exam_id",
        column2="student_id",
        string="Exam Name",
    )

    result_name = fields.One2many(
        comodel_name="result.details", inverse_name="student_name", string="result"
    )

    teachers_count = fields.Integer(string="Teachers", compute="_count_of_teachers")
    subject_count = fields.Integer(string="Subjects", compute="_count_of_subjects")
    exam_count = fields.Integer("Exams", compute="_count_of_exams")

    # calculate age form the date of birth

    def _compute_age(self):
        for records in self:
            today = date.today()
            current_year = today.year

            if (
                records.birth_date.year > current_year - 50
                and records.birth_date.year < current_year - 10
            ):
                records.age = today.year - records.birth_date.year
            else:
                raise ValidationError("Enter valid birthdate")

    # count of teachers

    def _count_of_teachers(self):
        for record in self:
            record.teachers_count = self.env["teachers.details"].search_count(
                [("student_ids", "=", self.name)]
            )

    # count of subjects

    def _count_of_subjects(self):
        for record in self:
            record.subject_count = self.env["subject.details"].search_count(
                [("student_ids", "=", self.name)]
            )

    # count of exams

    def _count_of_exams(self):
        for record in self:
            record.exam_count = self.env["exam.details"].search_count(
                [("student_ids", "=", self.name)]
            )

    # set student id as unique

    _sql_constraints = [
        (
            "unique_student_id",
            "unique(student_id)",
            "Student id Must be unique",
        ),
    ]

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
                "context": {},
                "domain": [("student_ids", "=", self.name)],
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
                "domain": [("student_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # view exam details

    def action_view_exam(self):
        if self.exam_count == 1:
            return {
                "name": "Exams",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "exam.details",
                "res_id": self.exam_ids.id,
                "target": "new",
            }
        else:
            return {
                "name": "Exams",
                "res_model": "exam.details",
                "view_mode": "tree,form",
                "context": {},
                "domain": [("student_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    def action_view_result(self):
        pass

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

    # sequence of student id

    @api.model
    def create(self, vals):
        vals["student_id"] = self.env["ir.sequence"].next_by_code("studentid.sequence")
        return super(StudentDetails, self).create(vals)

    # update name using write method

    @api.onchange("name")
    def update_father_name(self):
        for record in self:
            if record.name == "jainam":
                record.write({"father_name": "Kamleshbhai"})

    # restrict for delete record using ORM unlink method

    def unlink(self):
        for record in self:
            if record.exam_ids:
                raise UserError(("You cannot Delete this record"))
        return super(StudentDetails, self).unlink()

    # ORM name get method for display name for many2many tags

    def name_get(self):
        res = []
        for records in self:
            res.append((records.id, "%s, %s" % (records.student_id, records.name)))
        return res

    # ORM name search method for serch student name using multiple field values

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                "|",
                ("name", operator, name),
                ("phone_number", operator, name),
                ("father_name", operator, name),
            ]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        return super(StudentDetails, self).read(fields=fields, load=load)

