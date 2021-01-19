# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RentalReport(models.Model):

    _name = 'rental.report'

    vehicle_id = fields.Many2one('rent.request', 'Vehicle')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    def action_report_pdf(self):
        data = {
            'model_id': self.id,
        }
        return self.env.ref('rent.request.rental_report').report_action(self, data=data)

    @api.model
    def _get_report_values(self, docids, data):
        model_id = data['model_id']
        value = []
        query = """ SELECT *FROM rent_request """
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }