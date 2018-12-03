from functools import wraps
from flask import session, redirect, url_for
import config

def login_required(func):

    @wraps(func)
    def new_func(*args, **kwargs):
        user_id = session.get(config.USER_ID)
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.login'))
    return new_func

