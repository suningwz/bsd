# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
import logging
import re, os
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_purchase_tax = fields.Integer("TAXE ACHAT")
    x_studio_supplier_reference = fields.Char("Supplier Reference")
    x_studio_sale_tax = fields.Integer("TAXE VENTE")
    x_studio_supplier_name = fields.Char("NOM FOURN")
    x_studio_sub_categ_id = fields.Char("NOM COLLECTION")
    x_studio_incoterm = fields.Char("TRANSPORT")
    x_studio_catalog = fields.Char("CATALOGUE")
    x_studio_supplier_country = fields.Char("PAYS D'ORIGINE")
    x_studio_packing_mode = fields.Char("PACKING MODE")
    x_studio_gr = fields.Char("GR.")
    x_studio_internet = fields.Boolean("INTERNET")
    x_studio_image = fields.Boolean("IMAGE")
    x_studio_fost = fields.Integer("FOST+")
    x_studio_change = fields.Float("CHANGE")
    x_studio_inventory_value = fields.Float("VAL.INVENTAI")
    x_studio_percent_cost = fields.Float("% FRAIS")
    x_studio_uv_given = fields.Float("UV FOURNIS")
    x_studio_uv_bsd = fields.Float("UV BSD/ETIQ")
    x_studio_pr_brut = fields.Float("PR BRUT/FAC")
    x_studio_percent_remise = fields.Float("% REMISE")
    x_studio_pa_eur = fields.Float("PA EUR")
    x_studio_pa_usd = fields.Float("PA USD")
    x_studio_pa_shilling = fields.Float("PA SHILLING")
    x_studio_pa_sterling = fields.Float("PA STERLING")
    x_studio_fs_suisse = fields.Float("PA FS suiss")
    x_studio_pr_eur = fields.Float("P.R. EUR")
    x_studio_marge_benef = fields.Float("Marge bénéf")
    x_studio_marge_box = fields.Float("Marge Carton")
    x_studio_marge_indu = fields.Float("Marge Indu")
    x_studio_gropack_price = fields.Float("Prix Gropack")
    x_studio_pu_eur = fields.Float("P.U. Euro")
    x_studio_uv_box = fields.Float("U.V. Carton")
    x_studio_pv_ctn = fields.Float("P.V. Ctn")
    x_studio_pv_indu = fields.Float("P.V. Indu")
    x_studio_uv_remise = fields.Float("U.V.Remise")
    x_studio_pv_remise = fields.Float("P.V.Remise")
    x_studio_uv_palette = fields.Float("U.V.Palette")
    x_studio_prix_promo = fields.Float("PRIX PROMO")
    x_studio_col = fields.Float("COL.")
    x_studio_p_vidange = fields.Float("P.VIDANGE")
    x_studio_condit = fields.Float("CONDIT.")
    x_studio_has_tag = fields.Boolean("ETIQUETTE")
    x_studio_net_weight = fields.Float("POIDS NET")
    x_studio_brut_weight = fields.Float("POIDS BRUT")
    x_studio_qty_in_stock = fields.Float("QT. EN STOCK")
    x_studio_reserved_qty = fields.Float("QT. RESERVEE")
    x_studio_customer_order_qty = fields.Float("QT. COM. CLI")
    x_studio_supplier_order_qty = fields.Float("QT. COM. FOU")
    x_studio_deb_pro_ve = fields.Char("DEB PRO VE")
    x_studio_fin_pro_ve = fields.Char("FIN PRO VE")
    x_studio_pro_ach_price = fields.Char("PRIX PRO ACH")
    x_studio_deb_pro_ac = fields.Char("DEB PRO AC")
    x_studio_fin_pro_ac = fields.Char("FIN PRO AC")
    x_studio_categ_id = fields.Char("Ex Old NUMERO 2")
    x_studio_version = fields.Char("Saison")
    x_studio_uom_id = fields.Char("UoM")
    x_studio_uom_po_id = fields.Char("UoM Po")
    x_studio_commodity_code = fields.Char("Commodity code")
    x_studio_pv_euro = fields.Char("P.V. Euro")
    x_studio_nl_label = fields.Char("NL Label")
    x_studio_en_label = fields.Char("EN Label")
    x_studio_ge_label = fields.Char("GE Label")
    x_studio_c_douane = fields.Char("CDOUANE")
    x_studio_purchase_account = fields.Char("COMPTE ACHAT")
    x_studio_sale_account = fields.Char("COMPTE VENTE")
    x_studio_tc_label = fields.Char("LIBELLE TCHEQUE")

    def import_images(self):
        test_for_regex =  "237 9409925 GA.png.jpg"
        product_ids = self.search([('default_code', '!=', False)])
        base_url = "/home/odoo-admin/odoo_addons/vrac/"
        for product_id in product_ids[0:9]:
            if not product_id.image_1920:
                ref_no_wildcard = ''.join(product_id.default_code.split('*'))
                regex = ""
                for c in ref_no_wildcard:
                    regex += c
                    regex += "\s*"
                regex += "[.png|.jpg|.png.jpg|.PNG|.JPG|.PNG.JPG|.JPG.PNG|.jpg.png]{1}"
                pattern = re.compile(regex)
                for root, dirs, files in os.walk(base_url):
                    for file in files:
                        if pattern.match(file):
                            _logger.info(file)
                url_ref = base_url + regex


