# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Import Pdf Simple",
    "version": "15.0.1.0.0",
    "website": "https://github.com/OCA/edi",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base_import_pdf_simple",
        "sale_management",
        "product_supplierinfo_for_customer",
    ],
    "installable": True,
    "demo": [
        "demo/demo_synthesia.xml",
        "demo/demo_henkel.xml",
        "demo/demo_neklar.xml",
        "demo/demo_draxton.xml",
    ],
}
