# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RentalReport(models.Model):
    _name = 'report.vehicle_rental.rental_report'

    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle")
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    def action_report_pdf(self):
        data = {
            'model_id': self.id,
            'to_date': self.to_date,
            'from_date': self.from_date,
            'vehicle_id': self.vehicle_id.id,
            'vehicle_name': self.vehicle_id.vehicle_name
        }
        return self.env.ref('vehicle_rental.print_report_pdf').report_action(
            self,
            data=data)

    @api.model
    def _get_report_values(self, docids, data):
        model_id = data['model_id']
        from_date = data['from_date']
        to_date = data['to_date']
        vehicle_id = data['vehicle_id']
        vehicle_name = data['vehicle_name']

        print(to_date)
        print(from_date)
        print(model_id)
        print(vehicle_id)
        print(vehicle_name)

        value = []
        if  vehicle_name and from_date and to_date:
            query = """SELECT rent.vehicle_id, customer_id, from_date, to_date,
            rent.state, customer.name, vehicle.vehicle_id, vehicle.model,
            vehicle.vehicle_name
            FROM rent_request as rent
            INNER JOIN res_partner as customer
            ON rent.customer_id = customer.id
            INNER JOIN vehicle_rental as vehicle
            ON rent.vehicle_id = vehicle.id
            WHERE CAST(rent.from_date AS DATE) >=
            CAST('%s' AS DATE) AND CAST(rent.to_date AS DATE)
            <=  CAST('%s' AS DATE) AND rent.vehicle_id = %s""" % (
            from_date, to_date, vehicle_id)

        elif vehicle_name:
            query = """SELECT rent.vehicle_id, customer_id, from_date, to_date,
            rent.state, customer.name, vehicle.vehicle_id, vehicle.model,
            vehicle.vehicle_name
            FROM rent_request as rent
            INNER JOIN res_partner as customer
            ON rent.customer_id = customer.id
            INNER JOIN vehicle_rental as vehicle
            ON rent.vehicle_id = vehicle.id
            WHERE rent.vehicle_id = %s""" % (vehicle_id)

        elif from_date and to_date:
            query = """SELECT rent.vehicle_id, customer_id, from_date, to_date,
            rent.state, customer.name, vehicle.vehicle_id, vehicle.model,
            vehicle.vehicle_name
            FROM rent_request as rent
            INNER JOIN res_partner as customer
            ON rent.customer_id = customer.id
            INNER JOIN vehicle_rental as vehicle
            ON rent.vehicle_id = vehicle.id
            WHERE CAST(rent.from_date AS DATE) >=
            CAST('%s' AS DATE) AND CAST(rent.to_date AS DATE)
            <=  CAST('%s' AS DATE)""" % (from_date, to_date)

        else:
            query = """SELECT rent.vehicle_id, customer_id, from_date, to_date,
            rent.state, customer.name, vehicle.vehicle_id, vehicle.model,
            vehicle.vehicle_name
            FROM rent_request as rent
            INNER JOIN res_partner as customer
            ON rent.customer_id = customer.id
            INNER JOIN vehicle_rental as vehicle
            ON rent.vehicle_id = vehicle.id"""

        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        print(record)
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }
