import urllib2
import urllib
import hashlib

from odoo import models, api, tools

def download_gravatar(email, icon_set):
    gravatar_url = 'http://www.gravatar.com/avatar/' + \
                   hashlib.md5(email.lower()).hexdigest() + '?' + \
                   urllib.urlencode({'d': icon_set, 's': '128'})

    return urllib2.urlopen(gravatar_url, timeout=200).read()


class GravatarPartner(models.Model):
    _inherit = 'res.partner'

    # Override
    @api.model
    def create(self, values):
        if bool(values.get('email')) and not bool(values.get('image')):
            values['image'] = self._fetch_and_process_gravatar(values.get('email'), values.get('is_company'))

        return super(GravatarPartner, self).create(values)

    @api.multi
    @api.onchange('email')
    def _email_download_gravatar(self):
        for p in self:
            p._gravatar_update_image()

    @api.multi
    @api.onchange('image')
    def _image_download_gravatar(self):
        for p in self.filtered(lambda r: not bool(r.image)):
            p._gravatar_update_image()


    def _gravatar_update_image(self):
        """
        single record update
        """
        if bool(self.email):
            self.image = self._fetch_and_process_gravatar(self.email, self.is_company)
        else:
            self.image = super(GravatarPartner, self)._get_default_image(self.type, self.is_company, self.parent_id)

    def _fetch_and_process_gravatar(self, email, is_company):
        """
        Functional hook to return a properly 'odoo' formatted image
        :param email: string
        :param is_company: boolean
        :return: image suitable for attachment
        """
        gravatar_set = self._load_icon_config(is_company)
        image = download_gravatar(email, gravatar_set)
        if image:
            return tools.image_resize_image_big(image.encode('base64'))
        return False

    def _load_icon_config(self, is_company):
        config = self.env['ir.config_parameter'].sudo()
        key = 'gravatar.icon_set'
        if is_company:
            key += '.company'

        gravatar_config = config.search([('key', '=', key)])
        if not gravatar_config:
            gravatar_config = config.create({'key': key, 'value': 'identicon'})
        return gravatar_config.value