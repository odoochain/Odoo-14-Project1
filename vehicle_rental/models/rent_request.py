# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class RentRequest(models.Model):
    _name = 'rent.request'
    _description = 'Rent Request'
    _inherit = 'mail.thread'
    _rec_name = 'sequence'

    sequence = fields.Char(string="Number", readonly=True, required=True,
                       copy=False, default='New')
    customer_id = fields.Many2one('res.partner', string="Customer Name",
                                  track_visibility='always')
    request_date = fields.Date('Request Date', default=fields.Date.today)
    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle",
                                 track_visibility='always',domain=[(
                                 'state', '=', 'available')])
    from_date = fields.Date('From date')
    to_date = fields.Date('To date')
    period = fields.Integer(string='Period', default=1)
    period_type = fields.Many2one('rent.charges', string='Period Type')
    unit = fields.Float(string='Units', default=1)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    rent_request = fields.Monetary(string='Rent', related='period_type.amount')
    rent_total = fields.Monetary(string="Total Rent", compute='_compute_rent',
                                 store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('invoiced', 'Invoiced'),
         ('returned', 'Returned')], string="State", default='draft',track_visibility='always')
    warning = fields.Boolean(string='Warning', default=False,
                             compute="_compute_warning")
    late = fields.Boolean(string='Late', default=False,
                          compute="_compute_late")
    invoice_id = fields.Many2one('account.move', string="Invoice")
    is_paid = fields.Boolean(string='paid', default=False,
                             compute="_compute_paid")

    def _compute_warning(self):
        """ compute warning """
        for rec in self:
            rec.warning = rec.state == 'confirm' and rec.to_date and (
                    rec.to_date - fields.Date.today()).days <= 2

    def _compute_late(self):
        """ compute late """
        for rec in self:
            rec.late = rec.state == 'confirm' and rec.to_date and (
                    rec.to_date < fields.Date.today())

    def _compute_paid(self):
        """ checking paid status of invoice """
        for rec in self:
            rec.is_paid = rec.invoice_id.payment_state == 'paid'

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        """ compute period type based on current vehicle domain """
        for rec in self:
            return {'domain': {
                'period_type': [('vehicle_id', '=', rec.vehicle_id.id)]}}

    @api.depends('unit', 'period_type')
    def _compute_rent(self):
        """ compute quantity of period type """
        self.write(
            {'rent_total': self.period_type.amount * self.unit})

    @api.onchange('from_date', 'to_date')
    def _onchange_get_period(self):
        """ compute period """
        for rec in self.filtered(lambda l: l.from_date and l.to_date and (
                l.from_date <= l.to_date)):
            rec.period = (rec.to_date - rec.from_date).days + 1

    @api.model
    def create(self, vals):
        """ Sequence number generation """
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.rental.sequence') or 'New'
        result = super(RentRequest, self).create(vals)
        return result

    @api.constrains('to_date', 'from_date')
    def date_check(self):
        """ Date validation"""
        for rec in self.filtered(lambda l: l.to_date < l.from_date):
            raise ValidationError('Sorry Invalid Date!!')

    def action_confirm(self):
        """ Confirm button action """
        for rec in self:
            rec.state = 'confirm'
            rec.vehicle_id.state = 'not_available'

    def action_return(self):
        """ Return button action """
        for rec in self:
            rec.state = 'returned'
            rec.vehicle_id.state = 'available'

    def action_invoice(self):
        """ Invoice creation """
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'l10n_in_gst_treatment':self.customer_id.l10n_in_gst_treatment,
            'date': self.to_date,
            'partner_id': self.customer_id.id,
            'currency_id': self.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env['product.product'].search(
                    [('name', '=','Rental Service' )]),
                'name': self.vehicle_id.vehicle_name,
                'price_unit': self.rent_total,

            })],
        })
        invoice.action_post()
        self.invoice_id = invoice.id
        for rec in self:
            rec.state = 'invoiced'

        return {'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': invoice.id
                }

    def action_invoice_smart(self):
        """ Invoice smart button """
        return {'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_id.id
                }


class RequestCharges(models.Model):
    _name = 'rent.charges'
    _description = 'Request Charges'
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
