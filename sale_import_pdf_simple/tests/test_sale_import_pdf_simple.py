# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from base64 import b64encode
from os import path

from odoo.tests import common


class TestSaleImportPdfSimple(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
        # Synthesia
        cls.partner_synthesia = cls.env.ref(
            "sale_import_pdf_simple.res_partner_synthesia"
        )
        cls.template_synthesia = cls.env.ref(
            "sale_import_pdf_simple.sale_order_synthesia"
        )
        cls.template_synthesia.write(
            {"auto_detect_pattern": r"(?<=Synthesia Technology Europe)[\S\s]*"}
        )
        cls.env.ref(
            "sale_import_pdf_simple.sale_order_synthesia_line_product_id"
        ).write(
            {
                "default_value": "%s,%s"
                % (
                    "product.product",
                    cls.env.ref("product.product_product_25").id,
                )
            }
        )
        # Henkel
        cls.partner_henkel = cls.env.ref("sale_import_pdf_simple.res_partner_henkel")
        cls.template_henkel = cls.env.ref("sale_import_pdf_simple.sale_order_henkel")
        cls.template_henkel.write(
            {"auto_detect_pattern": r"(?<=Henkel Iberica Operations)[\S\s]*"}
        )
        cls.product_henkel = cls.env.ref(
            "sale_import_pdf_simple.product_product_henkel"
        )
        cls.env.ref("sale_import_pdf_simple.sale_order_henkel_line_product_id").write(
            {
                "default_value": "%s,%s"
                % (
                    "product.product",
                    cls.product_henkel.id,
                )
            }
        )
        # Neklar
        cls.partner_neklar = cls.env.ref("sale_import_pdf_simple.res_partner_neklar")
        cls.template_neklar = cls.env.ref("sale_import_pdf_simple.sale_order_neklar")
        cls.template_neklar.write({"auto_detect_pattern": r"(?<=ESTAMP S.A.U.)[\S\s]*"})
        cls.product_neklar = cls.env.ref(
            "sale_import_pdf_simple.product_product_neklar"
        )
        cls.env.ref("sale_import_pdf_simple.sale_order_neklar_line_product_id").write(
            {
                "default_value": "%s,%s"
                % (
                    "product.product",
                    cls.product_neklar.id,
                )
            }
        )
        # Draxton
        cls.partner_draxton = cls.env.ref("sale_import_pdf_simple.res_partner_draxton")
        cls.template_draxton = cls.env.ref("sale_import_pdf_simple.sale_order_draxton")
        cls.template_draxton.write(
            {"auto_detect_pattern": r"(?<=DRAXTON BARCELONA)[\S\s]*"}
        )
        cls.product_draxton = cls.env.ref(
            "sale_import_pdf_simple.product_product_draxton"
        )
        cls.env.ref("sale_import_pdf_simple.sale_order_draxton_line_product_id").write(
            {
                "default_value": "%s,%s"
                % (
                    "product.product",
                    cls.product_draxton.id,
                )
            }
        )
        # Reca
        cls.partner_reca = cls.env.ref("sale_import_pdf_simple.res_partner_reca")
        cls.template_reca = cls.env.ref("sale_import_pdf_simple.sale_order_reca")
        cls.template_reca.write({"auto_detect_pattern": r"(?<=RECA)[\S\s]*"})
        cls.product_reca = cls.env.ref("sale_import_pdf_simple.product_product_reca")
        cls.env.ref("sale_import_pdf_simple.sale_order_reca_line_product_id").write(
            {
                "default_value": "%s,%s"
                % (
                    "product.product",
                    cls.product_reca.id,
                )
            }
        )

    def _data_file(self, filename, encoding=None):
        filename = "data/" + filename
        mode = "rt" if encoding else "rb"
        with open(path.join(path.dirname(__file__), filename), mode) as file:
            data = file.read()
            return b64encode(data)

    def _create_ir_attachment(self, filename):
        return self.env["ir.attachment"].create(
            {
                "name": filename,
                "datas": self._data_file(filename),
            }
        )

    def _create_wizard_base_import_pdf_upload(self, attachment):
        wizard = self.env["wizard.base.import.pdf.upload"].create(
            {
                "model": "sale.order",
                "attachment_ids": attachment.ids,
            }
        )
        return wizard

    def _get_attachments(self, record):
        return self.env["ir.attachment"].search(
            [("res_model", "=", record._name), ("res_id", "=", record.id)]
        )

    def test_import_synthesia(self):
        default_product = self.env.ref("product.product_product_25")
        attachment = self._create_ir_attachment("sale-order-synthesia.pdf")
        wizard = self._create_wizard_base_import_pdf_upload(attachment)
        res = wizard.action_process()
        self.assertEqual(res["res_model"], "sale.order")
        record = self.env[res["res_model"]].browse(res["res_id"])
        attachments = self._get_attachments(record)
        self.assertEqual(record.partner_id, self.partner_synthesia)
        self.assertEqual(record.client_order_ref, "4500187276")
        self.assertIn(default_product, record.mapped("order_line.product_id"))
        self.assertIn(attachment, attachments)
        self.assertEqual(len(record.order_line), 10)
        self.assertEqual(sum(record.order_line.mapped("product_uom_qty")), 44)

    def test_import_henkel(self):
        attachment = self._create_ir_attachment("sale-order-henkel.pdf")
        wizard = self._create_wizard_base_import_pdf_upload(attachment)
        res = wizard.action_process()
        record = self.env[res["res_model"]].browse(res["res_id"])
        attachments = self._get_attachments(record)
        self.assertEqual(record.partner_id, self.partner_henkel)
        self.assertIn(attachment, attachments)
        self.assertIn(self.product_henkel, record.mapped("order_line.product_id"))
        self.assertEqual(len(record.order_line), 3)
        self.assertEqual(sum(record.order_line.mapped("product_uom_qty")), 60)

    def test_import_neklar(self):
        attachment = self._create_ir_attachment("sale-order-neklar.pdf")
        wizard = self._create_wizard_base_import_pdf_upload(attachment)
        res = wizard.action_process()
        record = self.env[res["res_model"]].browse(res["res_id"])
        attachments = self._get_attachments(record)
        self.assertEqual(record.partner_id, self.partner_neklar)
        self.assertIn(attachment, attachments)
        self.assertIn(self.product_neklar, record.mapped("order_line.product_id"))
        self.assertEqual(len(record.order_line), 2)
        self.assertEqual(sum(record.order_line.mapped("product_uom_qty")), 20)

    def test_import_draxton(self):
        attachment = self._create_ir_attachment("sale-order-draxton.pdf")
        wizard = self._create_wizard_base_import_pdf_upload(attachment)
        res = wizard.action_process()
        record = self.env[res["res_model"]].browse(res["res_id"])
        attachments = self._get_attachments(record)
        self.assertEqual(record.partner_id, self.partner_draxton)
        self.assertIn(attachment, attachments)
        self.assertIn(self.product_draxton, record.mapped("order_line.product_id"))
        self.assertEqual(len(record.order_line), 3)
        self.assertEqual(sum(record.order_line.mapped("product_uom_qty")), 14)

    def test_import_reca(self):
        attachment = self._create_ir_attachment("sale-order-reca.pdf")
        wizard = self._create_wizard_base_import_pdf_upload(attachment)
        res = wizard.action_process()
        record = self.env[res["res_model"]].browse(res["res_id"])
        attachments = self._get_attachments(record)
        self.assertEqual(record.partner_id, self.partner_reca)
        self.assertIn(attachment, attachments)
        self.assertIn(self.product_reca, record.mapped("order_line.product_id"))
        self.assertEqual(len(record.order_line), 23)
        self.assertEqual(sum(record.order_line.mapped("product_uom_qty")), 92)

    def test_import_multi(self):
        attachments = self._create_ir_attachment("sale-order-synthesia.pdf")
        attachments += self._create_ir_attachment("sale-order-henkel.pdf")
        attachments += self._create_ir_attachment("sale-order-neklar.pdf")
        attachments += self._create_ir_attachment("sale-order-draxton.pdf")
        attachments += self._create_ir_attachment("sale-order-reca.pdf")
        wizard = self._create_wizard_base_import_pdf_upload(attachments)
        res = wizard.action_process()
        orders = self.env[res["res_model"]].search(res["domain"])
        self.assertEqual(len(orders), 5)
        partners = orders.mapped("partner_id")
        self.assertIn(self.partner_synthesia, partners)
        self.assertIn(self.partner_henkel, partners)
        self.assertIn(self.partner_neklar, partners)
        self.assertIn(self.partner_draxton, partners)
        self.assertIn(self.partner_reca, partners)
