from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class LibraryDetails(models.Model):
    _name = "library.details"
    _description = "Details about the library"
    _rec_name = "book_name"

    book_id = fields.Char(
        string="Book ID", required=True, index=True, copy=False, default="new"
    )
    book_name = fields.Char("Book Name")
    is_available = fields.Boolean(string="Is Available")
    date_returned = fields.Date(string="Return Date")
    borrow_date = fields.Datetime(
        string="Last Borrowed On", help="Enter a last borrow date"
    )
    state = fields.Selection(
        [
            ("not_avalible", "Not Available"),
            ("available", "Available"),
        ],
        string="State",
    )
    number_of_book = fields.Integer(string="Number of books")
    color = fields.Integer(string="Color")
    image = fields.Binary(string="Cover", help="Attach a book cover")
    average_rating = fields.Float(
        string="Average Rating", help="Give a ratings to book"
    )
    course_id = fields.Many2one(
        comodel_name="course.details", string="Course Name", required=True
    )
    student_ids = fields.Many2many(
        comodel_name="student.details",
        relation="book_student_rel",
        column1="student_id",
        column2="book_id",
        string="Student Name",
    )
    student_count = fields.Integer(string="Students", compute="_count_of_students")

    @api.depends("number_of_book")
    def action_return(self):
        self.number_of_book += 1
        self.state = "available"
        self.is_available = True

    @api.onchange("number_of_book")
    def action_borrow(self):
        self.number_of_book -= 1
        if self.number_of_book < 1:
            self.state = "not_avalible"
            self.is_available = False

    # check numbers of books
    @api.constrains("number_of_books")
    def _check_number_of_books(self):
        for records in self:
            if records.number_of_books < 0:
                raise ValidationError("Number of books must not be zero Nagative")

    # count of students

    def _count_of_students(self):
        for records in self:
            records.student_count = self.env["student.details"].search_count(
                [("book_ids", "=", self.book_name)]
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
            {
                "name": "Students",
                "res_model": "student.details",
                "view_mode": "tree,form",
                "domain": [("book_ids", "=", self.book_name)],
                "target": "current",
                "type": "ir.actions.act_window",
            }

    @api.model
    def create(self, vals):
        vals["book_id"] = self.env["ir.sequence"].next_by_code("bookid.sequence")
        return super(LibraryDetails, self).create(vals)

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("book_name", operator, name), ("book_id", operator, name)]
            return self._search(
                domain + args, limit=limit, access_rights_uid=name_get_uid
            )

    def unlink(self):
        for record in self:
            if record.student_ids:
                raise UserError(("You cannot Delete this record"))
            return super(LibraryDetails, self).unlink()

    @api.model
    def name_get(self):
        res = []
        for records in self:
            res.append((records.id, "%s,%s" % (records.book_id, records.book_name)))
        return res
