# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle_rental(models.Model):
    _name = 'vehicle_rental.vehicle_rental'
    _description = 'vehicle_rental.vehicle_rental'

    vehicle = fields.Many2one('fleet.vehicle', string="Vehicle")
    v_name = fields.Char(string='Name')
    brand = fields.Char(string='Brand')
    registration = fields.Date(string="Registration Date")
    model = fields.Char(string='Model')
    rent = fields.Char(string='Rent')
    state = fields.Char(string='State')



    #   value = fields.Integer()
    #     value2 = fields.Float(compute="_value_pc", store=True)

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
