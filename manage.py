from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from app import create_app
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel, BoardModel, PostModel, like_relation

app = create_app()
manager = Manager(app)
Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    '''创建cms用户'''
    user = cms_models.CmsUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('success in adding cms user')

@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    '''创建前台用户'''
    user = front_models.FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_role():
    #1.visitor:可以修改个人信息
    visitor = cms_models.CmsRole(name='访问者', desc='能访问相关数据，不能修改')
    visitor.permission = cms_models.CMSPermission.VISITOR

    #2.operator(可以修改个人信息，管理帖子，评论，前台用户)
    operator = cms_models.CmsRole(name='运营', desc='管理帖子，评论，及前台用户')
    operator.permission = cms_models.CMSPermission.VISITOR|cms_models.CMSPermission.POSTER|cms_models.CMSPermission.FRONTER|cms_models.CMSPermission.COMMENTER

    #3.admin(拥有绝大数权限）
    admin = cms_models.CmsRole(name='管理员', desc='拥有全部权限')
    admin.permission = cms_models.CMSPermission.VISITOR|cms_models.CMSPermission.POSTER|cms_models.CMSPermission.FRONTER|cms_models.CMSPermission.COMMENTER|cms_models.CMSPermission.BOARDER|cms_models.CMSPermission.CMSUSER

    #4.developer
    developer = cms_models.CmsRole(name='开发者')
    developer.permission = cms_models.CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()

@manager.option('-r', '--role', dest='role')
@manager.option('-e', '--email', dest='email')
def add_user_to_role(role, email):
    user = cms_models.CmsUser.query.filter_by(email=email).first()
    if user:
        role = cms_models.CmsRole.query.filter_by(name=role).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('角色设置成功')
        else:
            print('请输入正确的角色名')
    else:
        print('该用户不存在')


@manager.command
def create_test_post():
    for i in range(321):
        post = PostModel(title='post:{}'.format(i), content='content()'.format(i))
        board = BoardModel.query.first()
        author = front_models.FrontUser.query.first()
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print('Success adding test post')


if __name__ == '__main__':
    manager.run()