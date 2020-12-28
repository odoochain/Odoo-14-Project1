# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle_rental(models.Model):
    _name = 'vehicle_rental.vehicle_rental'
    _description = 'vehicle_rental.vehicle_rental'

    vehicle = fields.Many2one('fleet.vehicle', string="Vehicle")
    v_name = fields.Char(string='Name')
    brand = fields.Many2one('fleet.vehicle.model.brand', string="Brand")
    registration = fields.Date(string="Registration Date")
    model = fields.Char(string='Model')
    rent = fields.Float(string='Rent')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([('type1', 'Available'), ('type2', 'Not Available'), ('type3', 'Sold')], 'Type',
                             default='type1')


class fleet_inherit(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False)

    #   value = fields.Integer()
    #   value2 = fields.Float(compute="_value_pc", store=True)

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
