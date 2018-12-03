from flask import session, g, render_template
from .views import bp
import config
from .models import FrontUser

@bp.before_request
def before_request():
    user_id = session.get(config.USER_ID)
    if user_id:
        front_user = FrontUser.query.get(user_id)
        if front_user:
            g.front_user = front_user


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('front/404.html')