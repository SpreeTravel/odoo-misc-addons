from openerp import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    custom_styles = fields.Text()


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    custom_styles = fields.Text(related="website_id.custom_styles")
