# -*- coding: utf-8 -*-

from odoo import api, fields, models


class RentalReportWizard(models.TransientModel):
    _name = 'rental.wizard'

    vehicle_id = fields.Many2one('rent.request', 'Vehicle')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

