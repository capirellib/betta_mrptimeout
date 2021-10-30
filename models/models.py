# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MrpWorkorder(models.Model):
    
    _inherit = 'mrp.workorder'

    #mostrarbutton = fields.Boolean(store=False,default=False)

    def button_scrap(self):
        self.ensure_one()
        return {
            'name': ('Scrap'),
            'view_mode': 'form',
            'res_model': 'stock.scrap',
            'view_id': self.env.ref('stock.stock_scrap_form_view2').id,
            'type': 'ir.actions.act_window',
            'context': {'default_production_id': self.production_id.id,
                        'product_ids': (self.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')) | self.move_finished_ids.filtered(lambda x: x.state == 'done')).mapped('product_id').ids,
                        'default_company_id': self.production_id.company_id.id,
                        'module' : 'betta_mrp_scrap'
                        },
            'target': 'new',
        }

    def action_desecho(self):
        #self.mostrarbutton = True
        self.ensure_one()
        return {
            'name': ('Desechos'),
            'view_mode': 'tree',
            'res_model': 'stock.scrap',
            'domain':[('production_id', '=', self.production_id.id)],
            'type': 'ir.actions.act_window',
            'view_id' : False,
            'target': 'new',
            'flags': {'action_buttons': False},
            'context': {'module' : 'betta_mrp_scrap'},
            }


