# Assignment 2.01
#
# Odoo reads this file to build the Apps list. The app icon is
# static/description/icon.png, found by that exact path.
{
    "name": "Kawiil Financing",
    "summary": "Streamlines the loan application process for dealerships.",
    # Odoo splits this on "/", so the app is filed under a Financing group
    # inside Kawiil.
    "category": "Kawiil/Financing",
    # Odoo puts the series in front, so 1.0.0 is stored as 20.0.1.0.0.
    "version": "1.0.0",
    "author": "Odoo",
    # Assignment 2.03: product, for the motorcycle. It brings base with it.
    #
    # Assignment 4.01: add "contacts", the partner form you extend lives there.
    #
    # Assignment 4.02: add "mail". product already pulls it in, but a module
    # lists what it uses itself, it should not rely on another module's
    # dependencies staying the same.
    "depends": ["product"],
    # Odoo Proprietary License, the default for custom customer work.
    "license": "OPL-1",
    # XML and CSV files Odoo loads on install, in the order you list them.
    #
    # Register each file in the assignment that creates it, and only then.
    # Listing a file before its models exist crashes the install.
    #
    # Order is not cosmetic. Odoo resolves external ids as it reads, so a file
    # can only refer to something a file above it already created: security,
    # then data, then views, then the menu that points at them.
    #
    # The finished list, with the assignment that adds each line:
    #     "security/kawiil_financing_groups.xml",             2.07
    #     "security/ir.access.csv",                           2.07
    #     "data/ir_sequence_data.xml",                        3.07
    #     "views/loan_application_views.xml",                 2.06
    #     "views/loan_application_tag_views.xml",             2.09
    #     "views/loan_application_document_type_views.xml",   2.09
    #     "views/res_partner_views.xml",                      4.01
    #     "views/kawiil_financing_menu.xml",                  2.06
    "data": [
        "security/kawiil_financing_groups.xml",
        "security/ir.access.csv",
        "data/ir_sequence_data.xml",
        "views/loan_application_views.xml",
        "views/loan_application_tag_views.xml",
        "views/loan_application_document_type_views.xml",
        "views/kawiil_financing_menu.xml",
    ],
    # Sample records, loaded only when a database is created with demo data.
    # Configuration data before transactional data, so the loans can refer to
    # tags that already exist.
    "demo": [
        "demo/config_demo.xml",
        "demo/loan_demo.xml",
    ],
    # True gives the module its own top-level menu and makes it show up as an
    # app. False would make it a technical module that only extends others.
    "application": True,
}
