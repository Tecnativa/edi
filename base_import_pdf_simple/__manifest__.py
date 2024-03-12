# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Base Import Pdf Simple",
    "version": "15.0.1.0.0",
    "website": "https://github.com/OCA/edi",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["mail"],
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/base_import_pdf_template_line_views.xml",
        "views/base_import_pdf_template_views.xml",
        "wizards/wizard_base_import_pdf_preview_views.xml",
        "wizards/wizard_base_import_pdf_upload_views.xml",
    ],
    "demo": [
        "demo/base_import_pdf_template.xml",
    ],
    "external_dependencies": {
        "python": ["pdftotext", "pypdf"],
    },
    "assets": {
        "web.assets_backend": [
            "base_import_pdf_simple/static/src/**/*.js",
        ],
        "web.assets_qweb": [
            "base_import_pdf_simple/static/src/**/*.xml",
        ],
    },
    "maintainers": ["victoralmau"],
}
