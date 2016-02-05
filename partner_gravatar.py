import urllib2
import urllib
import hashlib

from openerp import models, api, tools

def download_gravatar(email, icon_set):
    gravatar_url = 'http://www.gravatar.com/avatar/' + \
                   hashlib.md5(email.lower()).hexdigest() + '?' + \
                   urllib.urlencode({'d': icon_set, 's': '128'})

    return urllib2.urlopen(gravatar_url, timeout=200).read()


class GravatarPartner(models.Model):
    _inherit = 'res.partner'

    # Override
    @api.model
    def _get_default_image(self, is_company, colorize=False):
        return False

    # Override
    @api.model
    def create(self, values):
        new_partner = super(GravatarPartner, self).create(values)
        if not bool(new_partner.image):
            new_partner._gravatar_update_image()

        return new_partner

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
        if bool(self.email):
            gravatar_set = self._load_icon_config()
            image = download_gravatar(self.email, gravatar_set)
            if image:
                self.image = tools.image_resize_image_big(image.encode('base64'))
        else:
            self.image = super(GravatarPartner, self)._get_default_image(bool(self.is_company), True)

    def _load_icon_config(self):
        config = self.env['ir.config_parameter'].sudo()
        key = 'gravatar.icon_set'
        if self.is_company:
            key += '.company'

        gravatar_config = config.search([('key', '=', key)])
        if not gravatar_config:
            gravatar_config = config.create({'key': key, 'value': 'identicon'})
        return gravatar_config.value;