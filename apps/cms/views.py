from flask import Blueprint, views, render_template, request, session, redirect, url_for, g
from .forms import LoginFrom, ResetpwdForm, ResetemailForm, BannerForm, UpdataBannerForm, AddBoardForm, UpdateBoardForm
from .models import CmsUser, CMSPermission
from ..models import BannerModel, BoardModel, PostModel, HighlightPost
from .decorator import login_required, permission_required
import config
from exts import db, mail
from utils import restful, bbscache
from flask_mail import Message
import string, random

bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('email_captcha')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请输入邮箱参数')

    #set captcha
    source = list(string.ascii_letters)
    source.extend([str(i) for i in range(10)])
    captcha = ''.join(random.sample(source, 4))
    #send email
    message = Message('BBS邮箱验证', recipients=[email], body='your email captcha is {}'.format(captcha))
    try:
        mail.send(message)
    except:
        return restful.server_error('请稍后再试')
    bbscache.set(email, captcha)
    return restful.success()


@bp.route('/')
@login_required
def index():
    return render_template('cms/index.html')


@bp.route('/logout/')
@login_required
def logout():
    session.pop(config.CMS_USER_ID)
    return redirect(url_for('cms.cms_login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/profile.html')


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/banners.html', banners=banners)


@bp.route('/add_banner/', methods=['POST'])
@login_required
def add_banners():
    form = BannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/update_banner/', methods=['POST'])
@login_required
def updata_banners():
    form = UpdataBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('轮播图不存在')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/del_banner/', methods=['POST'])
@login_required
def del_banner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图ID')

    banner = BannerModel.query.get(banner_id)
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message='找不到该轮播图')


@bp.route('/posts/')
@permission_required(CMSPermission.POSTER)
@login_required
def posts():
    posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    return render_template('cms/posts.html', posts=posts)


@bp.route('/hl_post/', methods=['POST'])
@permission_required(CMSPermission.POSTER)
@login_required
def hl_post():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error('没有传入帖子ID')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('该帖子不存在')
    highlight = HighlightPost()
    highlight.post = post
    db.session.add(post)
    db.session.commit()
    return restful.success()


@bp.route('/unhl_post/', methods=["POST"])
@permission_required(CMSPermission.POSTER)
@login_required
def unhl_post():
    post_id = request.form.get('post_id')
    print(post_id)
    if not post_id:
        return restful.params_error('没有传入帖子ID')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error('该帖子不存在')
    highlight = HighlightPost.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/comments/')
@permission_required(CMSPermission.COMMENTER)
@login_required
def comments():
    return render_template('cms/comments.html')


@bp.route('/boards/')
@permission_required(CMSPermission.BOARDER)
@login_required
def boards():
    board_models = BoardModel.query.all()
    return render_template('cms/boards.html', boards=board_models)


@bp.route('/add_board/', methods=['POST'])
@permission_required(CMSPermission.BOARDER)
@login_required
def add_board():
    form = AddBoardForm(request.form)
    if form.validate():
        board_name = form.name.data
        board = BoardModel.query.filter_by(name=board_name).first()
        if not board:
            board = BoardModel(name=board_name)
            db.session.add(board)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('板块已存在')
    else:
        return restful.params_error(form.get_error())


@bp.route('/update_board/', methods=['POST'])
@permission_required(CMSPermission.BOARDER)
@login_required
def update_board():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        board_name = form.name.data
        board = BoardModel.query.get(board_id)
        if not board:
            return restful.params_error('该板块不存在')
        board.name = board_name
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/del_board/', methods=['POST'])
@permission_required(CMSPermission.BOARDER)
@login_required
def del_board():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error('没有传递板块ID')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error('该板块不存在')
    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/users/')
@permission_required(CMSPermission.FRONTER)
@login_required
def fuser_manage():
    return render_template('cms/fuser_manage.html')


@bp.route('/cmsuser_manage/')
@permission_required(CMSPermission.CMSUSER)
@login_required
def cuser_manage():
    return render_template('cms/cuser_manage.html')


@bp.route('/cmsrole_manage/')
@permission_required(CMSPermission.ALL_PERMISSION)
@login_required
def crole_manage():
    return render_template('cms/crole_manage.html')


@bp.route('/resetpwd/', methods=['GET', 'POST'])
@login_required
def resetpwd():
    if request.method == 'GET':
        return render_template('cms/resetpwd.html')
    else:
        form = ResetpwdForm(request.form)
        if form.validate():
            old_password = form.old_password.data
            new_password = form.new_password.data
            if g.cms_user.check_password(old_password):
                g.cms_user.password = new_password
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='旧密码错误!')
        else:
            message = form.get_error()
            return restful.params_error(message=message)


class ResetemailView(views.MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/resetemail.html')

    def post(self):
        form = ResetemailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/login.html', message=message)

    def post(self):
        form = LoginFrom(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            cms_user = CmsUser.query.filter(CmsUser.email == email).first()
            if cms_user and cms_user.check_password(password):
                session[config.CMS_USER_ID] = cms_user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            return self.get(message='用户名或密码错误')
        else:
            #print(form.errors)#form.errors可能是一个生成器
            message = form.errors
            return self.get(message=message)

bp.add_url_rule('/login/', endpoint='cms_login', view_func=LoginView.as_view('cms_login'))
bp.add_url_rule('/resetemail/', endpoint='resetemail', view_func=ResetemailView.as_view('resetemail'))
