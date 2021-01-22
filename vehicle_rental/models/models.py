# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from datetime import datetime


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = 'Vehicle Rental'
    _rec_name = 'vehicle_name'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle",
                                 domain=[('state_id', '=', 3)], required=True)
    vehicle_name = fields.Char(string='Name', related='vehicle_id.name',
                               store=True)
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
        [('available', 'Available'), ('not_available', 'Not Available'),
         ('sold', 'Sold')], string="Status", default='available')

    request_ids = fields.One2many('rent.request', 'vehicle_id',
                                  string='Confirm Requests',
                                  domain=lambda self: [
                                      ('state', '!=', 'draft')])

    charge_ids = fields.One2many('rent.charges', 'vehicle_id',
                                 string='Rent Requests', limit=4)

    _sql_constraints = [
        ('user_vehicle_name', 'unique (vehicle_name)',
         'Vehicle name already exists!!')]

    @api.onchange('registration')
    def _onchange_registration(self):
        """ Getting model year """
        if self.registration:
            self.model = self.registration.strftime("%Y")


    @api.constrains('charge_ids')
    def period_check(self):
        """ Validation of period types """
        for rec in self:
            list = []
            for l in rec.charge_ids:
                if l.time in list:
                    raise ValidationError(_(
                        "'%s' period is duplicated! Check Properly!!",l.time))
                list.append(l.time)

    def vehicle_requests(self):
        """ Vehicle request smart button """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Requests',
            'view_mode': 'tree,form',
            'res_model': 'rent.request',
            'domain': [('vehicle_id', '=', self.id)],
            'context': "{'create': False}"
        }

class FleetInherit(models.Model):
    _inherit = 'fleet.vehicle'


    registration_date = fields.Date('Registration Date ', required=False)
