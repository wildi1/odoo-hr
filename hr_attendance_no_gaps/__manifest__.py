{
    "name": "HR Attendance No Gaps",
    "summary": "Creates missing attendance entries for tracking absence days",
    "description": """
        In Odoo if somebody does not create an attendance entry, e.g. the person was not present one day, than the
        time, does not get subtracted. So the present time is wrong.
        This module adds missing attendance entries on days where the entry is missing with zero duration to fix this.
        You can set a work start date on every employee starting from the entries will be added.
    """,
    "author": "sewisoft",
    "website": "https://www.sewisoft.de",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Human Resources/Attendances",
    "version": "16.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "hr_attendance"],
    "license": "LGPL-3",
    # always loaded
    "data": [
        "views/hr_attendance_view.xml",
        "views/hr_employee_view.xml",
        "data/cron.xml",
    ],
}
