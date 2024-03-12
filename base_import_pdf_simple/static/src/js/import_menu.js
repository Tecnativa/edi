odoo.define("base_import_pdf_simple.BaseImportPdfSimpleMenu", function (require) {
    "use strict";

    const FavoriteMenu = require("web.FavoriteMenu");
    const {useModel} = require("web.Model");
    const {Component} = owl;

    class BaseImportPdfSimpleMenu extends Component {
        constructor() {
            super(...arguments);
            this.model = useModel("searchModel");
        }
        openWizardBaseImportPdfUpload() {
            this.trigger("do-action", {
                action: "base_import_pdf_simple.action_wizard_base_import_pdf_upload",
                options: {
                    additional_context: {
                        default_model: this.model.config.modelName,
                    },
                },
            });
        }
        static shouldBeDisplayed() {
            return true;
        }
    }
    BaseImportPdfSimpleMenu.props = {};
    BaseImportPdfSimpleMenu.template = "BaseImportPdfSimple.ImportRecords";
    FavoriteMenu.registry.add(
        "base-import-pdf-simple-menu",
        BaseImportPdfSimpleMenu,
        1
    );
    return BaseImportPdfSimpleMenu;
});
