from odoo import models, fields, api


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Details about the exam"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, help="Enter a exam name")
    exam_id = fields.Char(
        string="Exam ID", required=True, index=True, copy=False, default="new"
    )
    exam_date = fields.Date(string="Date Of Exam", help="enter date of exam")
    duration = fields.Char(string="Duration")
    course_ids = fields.Many2one("course.details", string="Course Name", required=True)
    subject_ids = fields.Many2one(
        "subject.details", string="Subject Name", required=True
    )
    student_ids = fields.Many2many(
        "student.details",
        "exam_student_rel",
        "student_id",
        "exam_id",
        string="Student Name",
    )
    exam_type = fields.Char(string="exam Type")
    exam_marks = fields.Integer(string="Marks")

    student_count = fields.Integer(string="Students", compute="_count_of_students")

    # count of students

    def _count_of_students(self):
        for record in self:
            record.student_count = self.env["student.details"].search_count(
                [("exam_ids", "=", self.name)]
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
                "domain": [("exam_ids", "=", self.name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    # write type of exAM

    @api.onchange("duration")
    def write_exam_type(self):
        for records in self:
            if records.duration == "2 hours":
                records.write({"exam_type": "Intenal"})
            elif records.duration == "3 hours":
                records.write({"exam_type": "External"})
            else:
                records.write({"exam_type": None})

    @api.model
    def create(self, vals):
        vals["exam_id"] = self.env["ir.sequence"].next_by_code("examid.sequence")
        return super(ExamDetails, self).create(vals)
