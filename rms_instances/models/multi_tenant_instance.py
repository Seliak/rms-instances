from odoo import models, fields, api

class MultiTenantInstance(models.Model):
    _name = 'multi.tenant.instance'
    _description = 'Multi-Tenant Instance'

    email = fields.Char(string='Email', required=True)
    instance_url = fields.Char(string='Instance URL', readonly=True)
    instance_port = fields.Integer(string='Instance Port', readonly=True)
    state = fields.Selection([
        ('created', 'Created'),
        ('error', 'Error'),
    ], string='State', default='created')
    logs = fields.Text(string='Logs', readonly=True)
