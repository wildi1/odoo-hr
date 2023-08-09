from odoo import models


class HrLeave(models.Model):

    # Private Attributes
    _inherit = "hr.leave"

    # Default methods

    # Fields declaration

    # Compute, inverse, search

    # Constraints and onChanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods
    def action_approve(self):
        res = super(HrLeave, self).action_approve()
        self._update_overtime()
        return res

    def action_refuse(self):
        res = super(HrLeave, self).action_refuse()
        self._update_overtime()
        return res

    # Business methods
    def _update_overtime(self):
        for s in self:
            attendance_dates = self.env["hr.attendance"].search(
                [
                    ("check_in", ">=", s.date_from.date()),
                    ("check_out", "<=", s.date_to.date()),
                    ("employee_id", "=", s.employee_id.id),
                ]
            )
            attendance_dates._update_overtime()
