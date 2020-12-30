# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vehicle_rental(models.Model):
    _name = 'vehicle_rental.vehicle_rental'
    _description = 'vehicle_rental.vehicle_rental'
    _rec_name = 'v_name'

    vehicle = fields.Many2one('fleet.vehicle', string="Vehicle")
    v_name = fields.Char(string='Name', required=True)
    brand = fields.Many2one(string='Brand',related='vehicle.brand_id', readonly=True)
    registration = fields.Date(string='Registration Date',related='vehicle.registration_date',readonly=True)
    model = fields.Char(string='Model')
    rent = fields.Monetary(string='Rent')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    state = fields.Selection(
        [('Available', 'Available'), ('Not Available', 'Not Available'),
         ('Sold', 'Sold')], 'Status', default='Available')


class fleet_inherit(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False)
