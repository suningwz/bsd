# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    date_diponibility = fields.Date( 
        string    = _('Date de mise à disposition'),
        translate = True
    )



    
