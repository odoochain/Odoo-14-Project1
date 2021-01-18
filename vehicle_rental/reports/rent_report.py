# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RentalReport(models.Model):

    _name = 'rental.report'

    @api.model
    def _get_report_values(self, docids, data):
        model_id = data['model_id']
        value = []
        query = """ """
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }