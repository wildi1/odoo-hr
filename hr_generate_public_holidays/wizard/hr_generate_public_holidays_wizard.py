# Copyright 2023 sewisoft GmbH (https://sewisoft.de)
# See module's manifest file for License.
from odoo import api, fields, models, _
from datetime import datetime, time
import holidays

from odoo.tools import format_date, pytz


class HrGeneratePublicHolidaysWizard(models.TransientModel):
    # Private Attributes
    _name = "hr.generate.public.holidays.wizard"
    _description = "This model represents Hr Generate Public Holidays Wizard."

    @api.model
    def _lang_get(self):
        return self.env['res.lang'].get_installed()

    def _default_lang(self):
        return self.env.lang

    # Default methods
    def _default_year(self):
        return datetime.now().strftime("%Y")

    def _default_country_id(self):
        return self.env.user.company_id.country_id

    # Fields declaration
    years = fields.Char(
        string="Years",
        help="Comma separated list of years possible",
        default=lambda self: self._default_year(),
        required=True
    )

    lang = fields.Selection(
        string="Language",
        selection=_lang_get,
        default=lambda self: self._default_lang(),
        required=True
    )

    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        default=lambda self: self._default_country_id(),
        required=True
    )

    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
        domain="[('country_id', '=?', country_id)]",
    )

    public_holiday_count = fields.Integer(
        string="Count",
        compute="_compute_preview",
    )

    preview = fields.Text(
        string="Preview",
        compute="_compute_preview",
    )

    # Compute, inverse, search
    @api.depends("lang", "years", "country_id", "state_id")
    def _compute_preview(self):
        for s in self:
            holiday_strings = []
            for holiday in self.get_holidays():
                date_str = format_date(self.env, holiday[0])
                holiday_strings.append(date_str + " - " + holiday[1])
            s.public_holiday_count = len(holiday_strings)
            s.preview = "\n".join(holiday_strings)

    # Constraints and onChanges
    @api.onchange("country_id")
    def onchange_state_id(self):
        self.state_id = False

    # CRUD methods (and name_get, name_search, ...) overrides

    # Action methods

    # Business methods
    def generate_holidays(self):
        holiday_list = self.get_holidays()
        vals_list = []
        tz = pytz.timezone(self.env.user.tz) or pytz.utc
        for holiday in holiday_list:
            date_from = tz.localize(datetime.combine(holiday[0], time(0, 0, 0))).astimezone(pytz.UTC).replace(
                tzinfo=None)
            date_to = tz.localize(datetime.combine(holiday[0], time(23, 59, 59))).astimezone(pytz.UTC).replace(
                tzinfo=None)
            vals_list.append({
                "name": _(holiday[1]),
                "date_from": date_from,
                "date_to": date_to,
            })

        self.env["resource.calendar.leaves"].create(vals_list)

        return self.env.ref("hr_holidays.open_view_public_holiday").read()[0]

    def get_holidays(self):
        if self.years and self.country_id:
            years = self.years.split(',')
            state = self.state_id.code
            if state and "-" in state:
                state = state.split("-")[1]
            holiday_list = []
            for year in years:
                holiday_list.extend(
                    holidays.country_holidays(
                        years=int(year),
                        country=self.country_id.code,
                        subdiv=state,
                        language=self.lang.split("_")[0]
                    ).items()
                )
            return sorted(holiday_list, key=lambda x: x[0])
        return []
