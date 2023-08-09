from odoo import fields, models


class HrAttendance(models.Model):

    # Private Attributes
    _inherit = "hr.attendance"

    # Default methods

    # Fields declaration
    is_generated = fields.Boolean()

    # Compute, inverse, search

    # Constraints and onChanges

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
