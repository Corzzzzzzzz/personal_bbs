import config
from flask import session, g
from .models import CmsUser, CMSPermission
from .views import bp

@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session[config.CMS_USER_ID]
        cms_user = CmsUser.query.get(user_id)
        if cms_user:
            g.cms_user = cms_user

@bp.context_processor
def context_processor():
    return {'CMSPermission': CMSPermission}