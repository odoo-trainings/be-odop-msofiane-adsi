# Assignment 4.03: the bridge between Kawiil Financing and Sales.
#
# A bridge holds what only makes sense when both modules are installed, so
# neither of them has to depend on the other.
{
    "name": "Kawiil Financing - Sales",
    "summary": "Start a loan application from a confirmed sale order.",
    "category": "Kawiil/Financing",
    "version": "1.0.0",
    "author": "Odoo",
    "depends": ["sale", "kawiil_financing"],
    "license": "OPL-1",
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
    ],
    # Not an app of its own, it extends two that are. auto_install installs
    # it by itself as soon as both dependencies are installed.
    "application": False,
    "auto_install": True,
}
