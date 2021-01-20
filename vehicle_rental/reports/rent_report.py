# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RentalReport(models.Model):
    _name = 'report.vehicle_rental.rental_report'

    vehicle_id = fields.Many2one('rent.request', 'Vehicle')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    def action_report_pdf(self):
        data = {
            'model_id': self.id,
        }
        return self.env.ref('vehicle_rental.print_report_pdf').report_action(
            self,
            data=data)

    @api.model
    def _get_report_values(self, docids, data):
        model_id = data['model_id']
        print(model_id)
        value = []
        query = """SELECT*
        FROM rent_request as rent
        INNER JOIN res_partner as customer
        ON rent.customer_id = customer.id"""

        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        print(record)
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }
