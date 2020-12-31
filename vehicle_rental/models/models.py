# -*- coding: utf-8 -*-

from odoo import models, fields


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _rec_name = 'vehicle_name'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle",
                                 domain=[('state_id', '=', 3)])
    vehicle_name = fields.Char(string='Name', required=True)
    brand_id = fields.Many2one(string='Brand', related='vehicle_id.brand_id',
                               readonly=True, store=True)
    registration = fields.Date(string='Registration Date',
                               related='vehicle_id.registration_date',
                               readonly=True)
    model = fields.Char(string='Model')
    rent = fields.Monetary(string='Rent')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                    self: self.env.user.company_id.currency_id)
    state = fields.Selection(
        [('Available', 'Available'), ('Not Available', 'Not Available'),
         ('Sold', 'Sold')], 'Status', default='Available')
    _sql_constraints = [
        ('vehicle_name', 'unique (vehicle_name)',
         'Vehicle name already exists!!')]

class FleetInherit(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False)
