from odoo import models, api, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    property_payment_term_id = fields.Many2one('account.payment.term', readonly=False)
    category_id = fields.Many2many('res.partner.category', string='Tags',
                                   compute="_compute_category_industry_application", store=True)
    comment = fields.Html(string='Notes')
    industry_application = fields.Selection(
        [('workplace', 'Workplace'), ('correctional', 'Correctional'), ('government', 'Government')],
        string="Industry Application", default=None, compute="_compute_industry_application", readonly=False, store=True)

    @api.depends('partner_id.industry_application')
    def _compute_industry_application(self):
        for lead in self:
            if lead.partner_id.industry_application:
                lead.industry_application = lead.partner_id.industry_application
            else:
                lead.industry_application = None

    @api.depends('partner_id.category_id')
    def _compute_category_industry_application(self):
        for lead in self:
            if lead.partner_id:
                if lead.partner_id.category_id:
                    lead.category_id = lead.partner_id.category_id.ids
                else:
                    lead.category_id = False

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        if self.check_data():
            data = self.data_payload()
            if data:
                partner = self.env['res.partner'].search([('id', '=', self.partner_id.id)])
                if partner:
                    partner.write(data)
            return res
        else:
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
            'function': self.function,
            'country_id': self.country_id.id,
            'title': self.title.id,
            'website': self.website,
            'category_id': self.category_id.ids,
            'comment': self.comment,
            'industry_application': self.industry_application,
            'property_payment_term_id': self.property_payment_term_id.id,
        }
        return payload

    def check_data(self):
        if (self.street == self.partner_id.street) and (self.street2 == self.partner_id.street2) and (
                self.property_payment_term_id.id == self.partner_id.property_payment_term_id.id) \
                and (self.zip == self.partner_id.zip) and (self.mobile == self.partner_id.mobile) and (
                self.phone == self.partner_id.phone) and (self.state_id.id == self.partner_id.state_id.id) \
                and (self.city == self.partner_id.city) and (self.function == self.partner_id.function) and (
                self.website == self.partner_id.website) and (self.category_id.ids == self.partner_id.category_id.ids) \
                and (self.comment == self.partner_id.comment) and (self.title.id == self.partner_id.title.id) and (self.industry_application == self.partner_id.industry_application):
            return False
        else:
            return True
