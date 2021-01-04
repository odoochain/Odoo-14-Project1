# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _rec_name = 'vehicle_name'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle",
                                 domain=[('state_id', '=', 3)],required=True)
    vehicle_name = fields.Char(string='Name')
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

    @api.onchange('vehicle_id')
    def _onchange_vehicle_name(self):
        for rec in self:
            rec.vehicle_name = rec.vehicle_id.name

    @api.onchange('registration')
    def _onchange_reg_year(self):
        for rec in self:
            if rec.registration:
                rec.model=rec.registration.strftime("%Y")

    def vehicle_requests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles',
            'view_mode': 'tree',
            'res_model': 'rent.request',
            'domain': [('vehicle_id', '=', self.id)],
            'context': "{'create': False}"
        }


class RentRequest(models.Model):
    _name = 'rent.request'

    name = fields.Char(string="Sequence", readonly=True, required=True,
                       copy=False, default='New')
    customer_id = fields.Many2one('res.partner',string="Customer Name")
    request_date = fields.Date('Request Date', default=fields.Date.today)
    vehicle_id = fields.Many2one('vehicle.rental',string="Vehicle")
    from_date = fields.Date('From date')
    to_date = fields.Date('To date')
    period = fields.Char(string='Period')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    rent_request = fields.Monetary(string='Rent', related="vehicle_id.rent")
    state = fields.Selection(
        [('Draft', 'Draft'), ('Confirm', 'Confirm'),
         ('Returned', 'Returned')], 'State', default='Draft')
    time = fields.Selection(
        [('Hour', 'Hour'), ('Day', 'Day'),
         ('Week', 'Week'),('Month', 'Month')], 'Time', default='Hour')
    amount = fields.Monetary(string='Amount')


    @api.onchange('from_date','to_date')
    def _onchange_get_period(self):
        for rec in self:
            if rec.from_date and rec.to_date:
                if rec.from_date < rec.to_date:
                    rec.period = (rec.to_date-rec.from_date).days

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'vehicle.rental.sequence') or 'New'
        result = super(RentRequest, self).create(vals)
        return result

    @api.constrains('to_date','from_date')
    def date_check(self):
        for rec in self:
            if rec.to_date < rec.from_date:
                raise ValidationError(('Sorry Date Invalid'))

    def action_confirm(self):
        for rec in self:
            rec.state='Confirm'
            rec.vehicle_id.state='Not Available'

    def action_return(self):
        for rec in self:
            rec.state='Returned'
            rec.vehicle_id.state='Available'

class FleetInherit(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False)
