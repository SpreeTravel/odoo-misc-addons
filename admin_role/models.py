from openerp import SUPERUSER_ID as SID
from openerp import models, tools

import logging
_logger = logging.getLogger(__name__)


def _has_admin_role(pool, cr, uid):
    user_pool = pool.get('res.users')
    imd = pool.get('ir.model.data')

    user = user_pool.browse(cr, SID, uid)
    group_id = imd.xmlid_to_object(cr, SID, 'admin_role.group_admin')

    try:
        rc = group_id in user.groups_id
    except:
        rc = False

    return rc


class ir_model_access(models.Model):
    _inherit = 'ir.model.access'

    @tools.ormcache()
    def check(self, cr, uid, model, mode='read', raise_exception=True,
              context=None):

        if uid == SID:
            return True

        return _has_admin_role(self.pool, cr, uid) or \
               super(ir_model_access, self).check(cr, uid, model, mode=mode,
                                                  raise_exception=raise_exception,
                                                  context=context)


class res_users(models.Model):
    _inherit = 'res.users'

    @tools.ormcache(skiparg=2)
    def has_group(self, cr, uid, group_ext_id):
        rc = _has_admin_role(self.pool, cr, uid) or \
             super(res_users, self).has_group(cr, uid, group_ext_id)

        return rc


class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    def get_user_roots(self, cr, uid, context=None):
        _uid = uid
        if _has_admin_role(self.pool, cr, uid):
            _uid = SID
        
        return super(ir_ui_menu, self).get_user_roots(cr, _uid, context=context)
