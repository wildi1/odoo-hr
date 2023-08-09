from datetime import date, datetime, time
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import pytz


class HrEmployee(models.Model):
    # Private Attributes
    _inherit = "hr.employee"

    # Default methods

    # Fields declaration
    count_attendance_from = fields.Date()

    # Compute, inverse, search
    @api.depends(
        "attendance_ids", "attendance_ids.check_in", "attendance_ids.check_out"
    )
    def _compute_last_attendance_id(self):
        for employee in self:
            employee.last_attendance_id = self.env["hr.attendance"].search(
                [
                    ("employee_id", "=", employee.id),
                    "|",
                    ("check_out", "=", False),
                    ("worked_hours", ">", 0),
                ],
                limit=1,
            )

    # Constraints and onChanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    @api.model
    def action_cron_attendance_fill_gaps(self):
        employees = self.env["hr.employee"].search([("count_attendance_from", "!=", False)])
        for employee in employees:
            query, params = self._get_missing_attendance_query_params(employee)
            self.env.cr.execute(query, params)
            missing_dates = self.env.cr.fetchall()

            vals = []
            tz = pytz.timezone(employee._get_tz()) or pytz.utc

            for missing_date in missing_dates:
                check_date_utc = (
                    tz.localize(datetime.combine(missing_date[0], time(3, 0, 0)))
                    .astimezone(pytz.UTC)
                    .replace(tzinfo=None)
                )
                vals.append(
                    {
                        "check_in": check_date_utc,
                        "check_out": check_date_utc,
                        "employee_id": employee.id,
                        "is_generated": True,
                    }
                )

            if vals:
                self.env["hr.attendance"].create(vals)

    def _get_missing_attendance_query_params(self, employee):
        date_from_str = employee.count_attendance_from.strftime(DEFAULT_SERVER_DATE_FORMAT)
        date_to_str = date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
        query = """SELECT * FROM generate_series(%s, %s, interval '1_day') AS dates
                   WHERE dates NOT IN (SELECT DATE(check_in) FROM hr_attendance WHERE employee_id = %s)"""
        return query, (date_from_str, date_to_str, employee.id)
