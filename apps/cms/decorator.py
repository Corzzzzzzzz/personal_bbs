from functools import wraps
from flask import session, redirect, url_for, g
import config
from .models import CMSPermission

def login_required(func):

    @wraps(func)
    def new_func(*args, **kwargs):
        cms_user_id = session.get(config.CMS_USER_ID)
        if cms_user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.cms_login'))

    return new_func

def permission_required(permission):
    def permission_decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return new_func
    return permission_decorator

