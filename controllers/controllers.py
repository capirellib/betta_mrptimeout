# -*- coding: utf-8 -*-
# from odoo import http


# class /opt/odoo/sources/bettaMrpTimeOut(http.Controller):
#     @http.route('//opt/odoo/sources/betta_mrp_time_out//opt/odoo/sources/betta_mrp_time_out/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//opt/odoo/sources/betta_mrp_time_out//opt/odoo/sources/betta_mrp_time_out/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/opt/odoo/sources/betta_mrp_time_out.listing', {
#             'root': '//opt/odoo/sources/betta_mrp_time_out//opt/odoo/sources/betta_mrp_time_out',
#             'objects': http.request.env['/opt/odoo/sources/betta_mrp_time_out./opt/odoo/sources/betta_mrp_time_out'].search([]),
#         })

#     @http.route('//opt/odoo/sources/betta_mrp_time_out//opt/odoo/sources/betta_mrp_time_out/objects/<model("/opt/odoo/sources/betta_mrp_time_out./opt/odoo/sources/betta_mrp_time_out"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/opt/odoo/sources/betta_mrp_time_out.object', {
#             'object': obj
#         })
