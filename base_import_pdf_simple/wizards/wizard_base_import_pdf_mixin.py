# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
import logging
from tempfile import NamedTemporaryFile

import pdftotext
import pypdf

from odoo import _, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class WizardBaseImportPdfMixin(models.AbstractModel):
    _name = "wizard.base.import.pdf.mixin"
    _description = "Wizard Base Import Pdf Mixin"

    extraction_mode = fields.Selection(
        selection=[("pypdf", _("Pypdf")), ("pdftotext_lib", _("Pdftotext Lib"))],
        default="pypdf",
        string="Extraction mode",
    )
    attachment_id = fields.Many2one(comodel_name="ir.attachment")

    def _pdf_text_extraction_pdftotext_lib(self, fileobj):
        # pdftotext lib doc: https://github.com/jalan/pdftotext
        res = False
        try:
            res = []
            with open(fileobj.name, "rb") as pdf_file:
                pdf = pdftotext.PDF(pdf_file)
                for page in pdf:
                    res.append(page)
            logger.info("Text extraction made with pdftotext lib")
        except Exception as e:
            logger.warning("Text extraction with pdftotext lib failed. Error: %s", e)
        return res

    def _pdf_text_extraction_pypdf(self, fileobj):
        res = False
        try:
            res = []
            reader = pypdf.PdfReader(fileobj.name)
            for pdf_page in reader.pages:
                res.append(pdf_page.extract_text())
            logger.info("Text extraction made with pypdf")
        except Exception as e:
            logger.warning("Text extraction with pypdf failed. Error: %s", e)
        return res

    def simple_pdf_text_extraction(self, file_data):
        fileobj = NamedTemporaryFile("wb", prefix="odoo-simple-pdf-", suffix=".pdf")
        fileobj.write(file_data)
        method = "_pdf_text_extraction_%s" % self.extraction_mode
        res = False
        if hasattr(self, method):
            res = getattr(self, method)(fileobj)
        fileobj.close()
        if not res:
            raise UserError(_("Odoo could not extract the text from the PDF."))
        return res

    def _fallback_parse_pdf(self, file_data):
        return self.simple_pdf_text_extraction(file_data)

    def _parse_pdf(self, data=False):
        file_data = base64.b64decode(data or self.attachment_id.datas)
        parsed_item = self._fallback_parse_pdf(file_data)
        return parsed_item or {}

    def _parse_pdf_grouped(self):
        """In some cases we need to get the text in all possible extraction modes
        (e.g. when we do not know which template to apply)."""
        res = {}
        extraction_modes = dict(
            self._fields["extraction_mode"]._description_selection(self.env)
        )
        file_data = base64.b64decode(self.attachment_id.datas)
        for extraction_mode in list(extraction_modes.keys()):
            self.extraction_mode = extraction_mode
            res[extraction_mode] = self._fallback_parse_pdf(file_data)
        return res
