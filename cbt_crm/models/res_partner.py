from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    industry_application = fields.Selection(
        [('workplace', 'Workplace'), ('correctional', 'Correctional'), ('government', 'Government')],
        string="Industry Application", default=None)

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        data = self.data_payload()
        if data:
            opportunity = self.env['crm.lead'].search([('partner_id', '=', self.id)])
            if opportunity:
                for rec in opportunity:
                    if rec.check_data():
                        rec.write(data)
                    else:
                        return res
        return res

    def data_payload(self):
        payload = {
            'mobile': self.mobile,
            'phone': self.phone,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state_id': self.state_id.id,
            'zip': self.zip,
            'title': self.title.id,
            'function': self.function,
            'country_id': self.country_id.id,
            'website': self.website,
            'category_id': self.category_id.ids,
            'comment': self.comment,
            'industry_application': self.industry_application,
            'property_payment_term_id': self.property_payment_term_id.id,
        }
        return payload

    def check_data(self, opportunity):
        if (self.street == opportunity.street) and (self.street2 == opportunity.street2) and (
                self.property_payment_term_id.id == opportunity.property_payment_term_id.id) \
                and (self.zip == opportunity.zip) and (self.mobile == opportunity.mobile) and (
                self.phone == opportunity.phone) and (self.state_id.id == opportunity.state_id.id) \
                and (self.city == opportunity.city) and (self.function == opportunity.function) and (
                self.website == opportunity.website) and (self.category_id.ids == opportunity.category_id.ids) \
                and (self.comment == opportunity.comment) and (self.title.id== opportunity.title.id) and (self.industry_application == opportunity.industry_application):
            return False
        else:
            return True
