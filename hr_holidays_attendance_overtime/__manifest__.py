{
    "name": "HR Attendance Overtime Updater",
    "summary": """
        This module updates the overtime, by changing holiday entries.""",
    "author": "sewisoft",
    "website": "https://www.sewisoft.de",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Human Resources/Attendances",
    "version": "16.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "hr_attendance", "hr_holidays", "resource"],
    "license": "LGPL-3",
    "data": [
        "data/ir_action_data.xml",
    ],
}
