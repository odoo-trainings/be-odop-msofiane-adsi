# Assignment 2.01: initialize the kawiil_financing manifest.
#
# Fill in every value marked TODO below, then add the one file this module is
# still missing:
#
#   kawiil_financing/static/description/icon.png  your app icon. Both the file
#                                                 name and the folder path have
#                                                 to match exactly.
#
# Odoo reads this file to build the Apps list. Spelling matters throughout the
# module: two underscores on each side of __manifest__ and __init__. Get one
# wrong and Odoo skips the whole directory without saying why.
{
    # The app title in the Apps list. This is the text you search for when you
    # install the module.
    "name": "TODO",
    # One line saying what the module does, shown under the title.
    "summary": "TODO",
    # Where the app is filed in the Apps list. Odoo splits this on "/", so
    # "Parent/Child" files it under a Child group inside Parent.
    "category": "TODO",
    # This module's own version number. Odoo puts the series in front of it
    # for you, so 1.0.0 is stored as 20.0.1.0.0. Leave as is.
    "version": "1.0.0",
    # Leave as is.
    "author": "Odoo",
    # The modules Odoo must install before this one. "base" is the framework
    # itself, so every module depends on it.
    #
    # Assignment 2.03: this module starts linking to products, so swap "base"
    # for "product". Drop "base" when you do, product already depends on it
    # and Odoo installs the whole chain for you.
    #
    # Assignment 4.01: add "contacts", the partner form you extend lives there.
    #
    # Assignment 4.02: add "mail". product already pulls it in, but a module
    # lists what it uses itself, it should not rely on another module's
    # dependencies staying the same.
    "depends": ["base"],
    # Odoo Proprietary License, the default for custom customer work.
    "license": "OPL-1",
    # XML and CSV files Odoo loads on install, in the order you list them.
    #
    # Register each file in the assignment that creates it, and only then.
    # Listing a file before its models exist crashes the install, so add the
    # lines marked 2.06 when you get to 2.06, not now.
    #
    # Order is not cosmetic. Odoo resolves external ids as it reads, so a file
    # can only refer to something a file above it already created: security,
    # then data, then views, then the menu that points at them. The list grows
    # by insertion, not by appending: at 2.07 the security files go in above
    # the views you added at 2.06.
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
    #
    # Assignment 2.09: the three new models need access rows too. A CSV file
    # cannot hold comments, so they wait here instead. Copy these lines to the
    # end of security/ir.access.csv when you reach 2.09, not before: a row
    # for a model that does not exist yet stops the install.
    #
    #     access_loan_application_tag_user,loan.application.tag.user,True,model_loan_application_tag,group_kawiil_financing_user,r,,"Users pick tags on a loan, only admins manage the list."
    #     access_loan_application_tag_admin,loan.application.tag.admin,True,model_loan_application_tag,group_kawiil_financing_admin,crud,,"Admins manage the tag list."
    #     access_loan_application_document_type_user,loan.application.document.type.user,True,model_loan_application_document_type,group_kawiil_financing_user,r,,"Users see which documents a loan needs, only admins decide that."
    #     access_loan_application_document_type_admin,loan.application.document.type.admin,True,model_loan_application_document_type,group_kawiil_financing_admin,crud,,"Admins decide which documents a loan needs."
    #     access_loan_application_document_user,loan.application.document.user,True,model_loan_application_document,group_kawiil_financing_user,crud,,"Users fill in the compliance checklist of their loans."
    #     access_loan_application_document_admin,loan.application.document.admin,True,model_loan_application_document,group_kawiil_financing_admin,crud,,"Admins have full access to every checklist."
    "data": [],
    # Sample records, loaded only when a database is created with demo data.
    #
    # Same rule as above, one line per assignment, inserted in order.
    # Configuration data before transactional data, so the loans can refer to
    # tags that already exist:
    #     "demo/config_demo.xml",   2.09
    #     "demo/loan_demo.xml",     2.04
    "demo": [],
    # True gives the module its own top-level menu and makes it show up as an
    # app. False would make it a technical module that only extends others.
    "application": True,
}
