# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class RentRequest(models.Model):
    _name = 'rent.request'
    _inherit = 'mail.thread'

    name = fields.Char(string="Number", readonly=True, required=True,
                       copy=False, default='New', track_visibility='always')
    customer_id = fields.Many2one('res.partner', string="Customer Name",
                                  track_visibility='always')
    request_date = fields.Date('Request Date', default=fields.Date.today)
    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle",
                                 track_visibility='always')
    from_date = fields.Date('From date')
    to_date = fields.Date('To date')
    period = fields.Integer(string='Period', default=1)
    period_type = fields.Many2one('rent.charges', string='Period Type')
    unit = fields.Float(string='Units', default=1)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    rent_request = fields.Monetary(string='Rent', related='period_type.amount')
    rent_total = fields.Monetary(string="Total Rent", compute='compute_rent',
                                 store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('invoiced', 'Invoiced'),
         ('returned', 'Returned')], string="State", default='draft')
    warning = fields.Boolean(string='Warning', default=False,
                             compute="_compute_warning")
    late = fields.Boolean(string='Late', default=False,
                          compute="_compute_late")

    def _compute_warning(self):
        today = fields.Date.today()
        for rec in self:
            rec.warning = rec.state == 'confirm' and rec.to_date and (
                    rec.to_date - today).days == 2

    def _compute_late(self):
        today = fields.Date.today()
        for rec in self:
            rec.late = rec.state == 'confirm' and rec.to_date and rec.to_date < today

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        for self in self:
            return {'domain': {
                'period_type': [('vehicle_id', '=', self.vehicle_id.id)]}}

    @api.depends('unit', 'period_type')
    def compute_rent(self):
        self.write(
            {'rent_total': self.period_type.amount * self.unit})

    @api.onchange('from_date', 'to_date')
    def _onchange_get_period(self):
        for rec in self.filtered(lambda l: l.from_date and l.to_date and (
                l.from_date <= l.to_date)):
            rec.period = (rec.to_date - rec.from_date).days + 1

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'vehicle.rental.sequence') or 'New'
        result = super(RentRequest, self).create(vals)
        return result

    @api.constrains('to_date', 'from_date')
    def date_check(self):
        for rec in self.filtered(lambda l: l.to_date < l.from_date):
            raise ValidationError('Sorry Invalid Date!!')

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            rec.vehicle_id.state = 'not_available'

    def action_return(self):
        for rec in self:
            rec.state = 'returned'
            rec.vehicle_id.state = 'available'

    def action_invoice(self):
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'date': self.to_date,
            'partner_id': self.customer_id.id,
            'currency_id': self.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.vehicle_id.vehicle_name,
                'price_unit': self.rent_total,

            })],
        })
        for rec in self:
            rec.state = 'invoiced'

        return {'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id
                }

class RequestCharges(models.Model):
    _name = 'rent.charges'
    _rec_name = 'time'

    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle")
    time = fields.Selection(
        [('hour', 'Hour'), ('day', 'Day'),
         ('week', 'Week'), ('month', 'Month')], string="Time", default='hour',
        store=True)

    amount = fields.Monetary(string='Amount')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)

