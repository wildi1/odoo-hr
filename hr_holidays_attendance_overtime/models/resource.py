from odoo import models


class CalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    def unlink(self):
        attendance_dates = self._get_attendances()
        res = super(CalendarLeaves, self).unlink()
        attendance_dates._update_overtime()
        return res

    def _get_attendances(self):
        attendance_dates = self.env["hr.attendance"]
        for s in self:
            attendance_dates |= self.env["hr.attendance"].search(
                [
                    ("check_in", ">=", s.date_from.date()),
                    ("check_out", "<=", s.date_to.date()),
                ]
            )
        return attendance_dates
