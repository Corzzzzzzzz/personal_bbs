from flask import Blueprint, render_template, views, request, session, redirect, url_for, g, abort
from utils import restful, safe_utils
from .forms import SignInForm, LoginForm, PostAddForm, CommentAddForm, AccountModifyForm, SecurityForm
from .models import FrontUser
from ..models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPost
from exts import db
from .decorator import login_required
import config
from flask_paginate import get_page_parameter, Pagination


bp = Blueprint('front', __name__)


@bp.route('/')
def index():

    board_id = request.args.get('board_id', type=int, default=None)
    sort = request.args.get('sort', type=int, default=None)
    # 获取banner图信息及板块信息
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4).all()
    boards = BoardModel.query.all()
    # 获取界面页数，并设置从数据库中选择切片的索引
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    # 设置帖子排序方式
    # sort==1：先按有无加精，再按时间倒叙
    if sort == 1:
        obj = db.session.query(PostModel).outerjoin(HighlightPost).order_by(HighlightPost.id.desc(), PostModel.create_time.desc())
    # sort==2：先按点赞数，再按时间倒叙
    elif sort == 2:
        # obj = PostModel.query.outerjoin(like_relation).group_by(PostModel.id).order_by(db.func.count(like_relation).desc(), PostModel.create_time.desc())

        obj = PostModel.query.outerjoin(FrontUser).group_by(PostModel.id)
        print(obj)
        obj = obj.order_by(db.func.count(FrontUser.id).desc(), PostModel.create_time.desc())
    # sort==3：先按评论数，再按时间倒叙
    elif sort == 3:
        obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(db.func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    # 无sort参数：按时间倒叙
    else:
        obj = PostModel.query.order_by(PostModel.create_time.desc())
    # 安装板块筛选帖子，并根据页面索引切片
    if board_id:
        posts = obj.filter(PostModel.board_id == board_id).slice(start, end)
        total = PostModel.query.filter_by(board_id=board_id).count()
    else:
        posts = obj.slice(start, end)
        total = PostModel.query.count()

    pagination = Pagination(page=page, total=total, bs_version=3)
    content = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board_id': board_id
    }
    return render_template('front/index.html', **content)


@bp.route('/account/', methods=['POST', 'GET'])
@login_required
def account():
    if request.method == 'GET':
        return render_template('front/account.html')
    else:
        form = AccountModifyForm(request.form)
        if form.validate():
            # 获取用户信息的表单数据
            username = form.username.data
            email = form.email.data
            realname = form.realname.data
            signature = form.signature.data
            avatar_url = form.avatar_url.data
            # 从数据库中获取现在登陆的用户信息
            user = g.front_user
            # 判断用户是否提交了个人信息，若有则修改在数据库中
            if username:
                user.username = username
            if email:
                user.email = email
            if realname:
                user.realname = realname
            if signature:
                user.signature = signature
            user.avatar = avatar_url
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/security/', methods=['POST', 'GET'])
@login_required
def security():
    if request.method == 'GET':
        return render_template('front/security.html')
    else:
        form = SecurityForm(request.form)
        if form.validate():
            # 获取表单提交的新旧密码
            old_password = form.old_password.data
            password = form.password1.data
            # 获取登陆的用户信息
            user = g.front_user
            # 判断原密码是否和数据库一致， 若一致则修改
            if user.check_password(old_password):
                user.password = password
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error('原密码错误！')
        else:
            return restful.params_error(form.get_error())


@bp.route('/post/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    # 判断用户是否登陆
    try:
        user = g.front_user
    except:
        user = ''
    # 判断用户是否登陆，且改用户是否赞过这篇帖子
    if user and post.check_liker(user):
        like = True
    else:
        like = False

    content = {
        'post': post,
        'like': like
    }
    return render_template('front/post_detail.html', **content)


@bp.route('/add_post/', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/add_post.html', boards=boards)
    else:
        form = PostAddForm(request.form)
        if form.validate():
            title = form.title.data
            content = form .content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error('板块不存在')
            post = PostModel(title=title, content=content, board_id=board_id, author_id=g.front_user.id)
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


@bp.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    form = CommentAddForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content, post_id=post_id)
            comment.commenter = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        return restful.params_error('帖子不存在')
    return restful.params_error(form.get_error())


@bp.route('/delete_comment/', methods=['POST'])
@login_required
def delete_comment():
    comment_id = request.form.get('comment_id')
    if not comment_id:
        return restful.params_error('没有传递帖子ID')
    comment = CommentModel.query.get(comment_id)
    if not comment:
        return restful.params_error('该帖子不存在')
    if comment.commenter.id != g.front_user.id:
        return restful.params_error('呀！想删除其他人的帖子。不可能！')
    db.session.delete(comment)
    db.session.commit()
    return restful.success()


@bp.route('/inform_comment/', methods=['POST'])
@login_required
def inform_comment():
    pass


@bp.route('/like/', methods=["POST"])
@login_required
def add_like():
    post_id = request.form.get('post_id')
    print(post_id)
    if post_id:
        user = g.front_user
        post = PostModel.query.get(post_id)
        print(post)
        if post.check_liker(user):
            print(type(post.likers))
            post.likers.remove(user)
        else:
            post.likers.append(user)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error('没有传递帖子ID')


@bp.route('/personal/')
def personal():
    # 获取url的id参数，若无则认为是登陆者id，若都无则跳转到登陆界面
    try:
        user_id = request.args.get('id', g.front_user.id)
    except AttributeError:
        return redirect(url_for('front.login'))
    # 获取用户信息及关注者和被关注者信息
    user = FrontUser.query.get(user_id)
    if not user:
        abort(404)
    followed_lists = user.followed
    follower_lists = user.followers
    # 判断登陆用户和页面对应用户的关注关系
    relation = ''
    try:
        login_user = g.front_user
    except AttributeError:
        login_user = ''
    if login_user and login_user.is_following(user):
        relation = True

    content = {
        'user': user,
        'followed_lists': followed_lists,
        'follower_lists': follower_lists,
        'relation': relation
    }
    return render_template('front/personal.html', **content)


@bp.route('/add_follow_relation/', methods=['POST'])
@login_required
def add_followed_relation():
    # 获取登陆的用户
    follower = g.front_user
    # 获取要关注的用户ID
    followed_id = request.form.get('followed_id', None)
    # 判断被关注的用户是否存在
    if not followed_id:
        return restful.params_error('没有传递被关注者id')
    followed = FrontUser.query.get(followed_id)
    if not followed:
        return restful.params_error('用户不存在')
    # 判断用户直接是否已经操作关注关系，若有取消关注，无进行关注
    if follower.is_following(followed):
        follower.unfollow(followed)
    else:
        follower.follow(followed)
    db.session.commit()
    return restful.success()


class SignInView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safe_utils.is_safe_url(return_to):
            return render_template('front/sign_in.html', return_to=return_to)
        else:
            return render_template('front/sign_in.html')

    def post(self):
        form = SignInForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


class LoginView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.sign_in') and safe_utils.is_safe_url(return_to):
            return render_template('front/login.html', return_to=return_to)
        else:
            return render_template('front/login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember_me = form.remember_me.data

            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.USER_ID] = user.id

                if remember_me:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error('用户名或密码错误')

        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/sign_in/', view_func=SignInView.as_view('sign_in'))
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


@bp.route('/logout/')
@login_required
def logout():
    session.pop(config.USER_ID)
    return redirect(url_for('front.index'))