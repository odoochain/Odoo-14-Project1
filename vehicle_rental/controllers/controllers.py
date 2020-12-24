# -*- coding: utf-8 -*-
# from odoo import http


# class VehicleRental(http.Controller):
#     @http.route('/vehicle_rental/vehicle_rental/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vehicle_rental/vehicle_rental/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vehicle_rental.listing', {
#             'root': '/vehicle_rental/vehicle_rental',
#             'objects': http.request.env['vehicle_rental.vehicle_rental'].search([]),
#         })

#     @http.route('/vehicle_rental/vehicle_rental/objects/<model("vehicle_rental.vehicle_rental"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vehicle_rental.object', {
#             'object': obj
#         })
