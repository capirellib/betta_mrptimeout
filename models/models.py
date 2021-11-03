# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MrpWorkorder(models.Model):
    
    _inherit = 'mrp.workorder'
    
    show_ocio = fields.Integer(default=0)

    time_out =fields.Float(
    'Duracion Ocioso', digits=(16, 2) , default = 0,
    help="Duracion Tiempo Ocioso (en minutes)" )

    
    #calc_ocio = fields.Boolean(default=True) ##Permite Iniciar o Detener el RELOJ
    instanteInicial = fields.Datetime()

    #@api.onchange('time_out')
    def _compute_timeout(self):
        for order in self:
            timeline_obj = self.env['mrp.workcenter.productivity']
            domain = [('workorder_id', 'in', self.ids)]   
            self.time_out_total = 0
            for timeline in timeline_obj.search(domain):
                    self.time_out_total = timeline.time_out + self.time_out_total
            self.time_out_total = self.time_out_total +self.time_out
    

    time_out_total = fields.Float(
        'T.Ocioso', compute=_compute_timeout, store=False)
        #, inverse='_set_duration',
        #readonly=False, store=True, copy=False)

    
    def button_start(self):
        self.show_ocio = 1
        return super().button_start()


    def button_finish(self):
        if self.show_ocio == 2:
            self.button_Ocio()
        self.show_ocio = 0
        return super().button_finish()

    def button_pending(self):
        if self.show_ocio == 2:
            self.button_Ocio()
        self.show_ocio = 0
        return super().button_pending()


    def end_previous(self, doall=False):
        """
        @param: doall:  This will close all open time lines on the open work orders when doall = True, otherwise
        only the one of the current user
        """
        # TDE CLEANME
        timeline_obj = self.env['mrp.workcenter.productivity']
        domain = [('workorder_id', 'in', self.ids), ('date_end', '=', False)]
        if not doall:
            domain.append(('user_id', '=', self.env.user.id))
        not_productive_timelines = timeline_obj.browse()
        for timeline in timeline_obj.search(domain, limit=None if doall else 1):
            wo = timeline.workorder_id
            if wo.duration_expected <= wo.duration:
                if timeline.loss_type == 'productive':
                    not_productive_timelines += timeline

                timeline.write({'date_end': fields.Datetime.now() ,'time_out': self.time_out})
                self.time_out = 0
            else:
                maxdate = fields.Datetime.from_string(timeline.date_start) + relativedelta(minutes=wo.duration_expected - wo.duration)
                enddate = datetime.now()
                if maxdate > enddate:

                    timeline.write({'date_end': enddate ,'time_out': self.time_out})
                    self.time_out = 0
                else:

                    timeline.write({'date_end': maxdate })
                    not_productive_timelines += timeline.copy({'date_start': maxdate, 'date_end': enddate})
        if not_productive_timelines:

            loss_id = self.env['mrp.workcenter.productivity.loss'].search([('loss_type', '=', 'performance')], limit=1)
            if not len(loss_id):

                raise UserError(_("You need to define at least one unactive productivity loss in the category 'Performance'. Create one from the Manufacturing app, menu: Configuration / Productivity Losses."))

            not_productive_timelines.write({'loss_id': loss_id.id})
        self._compute_timeout()
        return True

    def button_Ocio(self):
        #instanteInicial = datetime.now()
        #instanteFinal = datetime.now()
        #tiempo = instanteFinal - instanteInicial # Devuelve un objeto timedelta
        #segundos = tiempo.seconds

        if self.show_ocio == 1 :
            self.instanteInicial = datetime.now()
            self.show_ocio = 2
        else:
            instanteFinal = datetime.now()    
            tiempo = instanteFinal - self.instanteInicial # Devuelve un objeto timedelta
            tiempo1 = tiempo / timedelta(minutes=1)
            self.time_out = tiempo1 + self.time_out    
            self.show_ocio = 1




#*********************************************************************************
#*********************************************************************************


class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    time_out = fields.Float(
        'Ocioso Total', digits=(16, 2),
        help="Duracion Tiempo Ocioso (en minutes)")    

    #time_out_total = fields.Float(
    #    'T.Ocioso', store=True)

    # def button_scrap(self):
    #     self.ensure_one()
    #     return {
    #         'name': ('Scrap'),
    #         'view_mode': 'form',
    #         'res_model': 'stock.scrap',
    #         'view_id': self.env.ref('stock.stock_scrap_form_view2').id,
    #         'type': 'ir.actions.act_window',
    #         'context': {'default_production_id': self.production_id.id,
    #                     'product_ids': (self.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')) | self.move_finished_ids.filtered(lambda x: x.state == 'done')).mapped('product_id').ids,
    #                     'default_company_id': self.production_id.company_id.id,
    #                     'module' : 'betta_mrp_scrap'
    #                     },
    #         'target': 'new',
    #     }

    # def action_desecho(self):
    #     #self.mostrarbutton = True
    #     self.ensure_one()
    #     return {
    #         'name': ('Desechos'),
    #         'view_mode': 'tree',
    #         'res_model': 'stock.scrap',
    #         'domain':[('production_id', '=', self.production_id.id)],
    #         'type': 'ir.actions.act_window',
    #         'view_id' : False,
    #         'target': 'new',
    #         'flags': {'action_buttons': False},
    #         'context': {'module' : 'betta_mrp_scrap'},
    #         }


