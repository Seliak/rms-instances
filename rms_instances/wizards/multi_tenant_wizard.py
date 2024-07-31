from odoo import models, fields
import subprocess

class MultiTenantWizard(models.TransientModel):
    _name = 'multi.tenant.wizard'
    _description = 'Multi-Tenant Wizard'

    email = fields.Char(string='Email', required=True)

    def create_instance(self):
        script_path = 'rms_instances/scripts/create_docker_instance.sh'
        email_hash = self.email.replace('@', '_').replace('.', '_')
        process = subprocess.Popen([script_path, self.email, email_hash], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        logs = out.decode('utf-8') + "\n" + err.decode('utf-8')
        
        if process.returncode == 0:
            docker_compose_file = out.decode('utf-8').strip()
            port = int(docker_compose_file.split('-')[-1].split('.')[0])
            instance = self.env['multi.tenant.instance'].create({
                'email': self.email,
                'instance_url': f'http://localhost:{port}',
                'instance_port': port,
                'logs': logs,
            })
        else:
            instance = self.env['multi.tenant.instance'].create({
                'email': self.email,
                'state': 'error',
                'logs': logs,
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Multi-Tenant Instance',
            'view_mode': 'form',
            'res_model': 'multi.tenant.instance',
            'res_id': instance.id,
            'target': 'new',
        }
