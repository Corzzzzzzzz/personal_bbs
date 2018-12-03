from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class CMSPermission():
    #使用8位二进制形式表示CMS用户权限(1111 1111)
    ALL_PERMISSION = 0b11111111
    #1.访问者权限
    VISITOR =        0b00000001
    #2.管理帖子的权限
    POSTER =         0b00000010
    #3.管理评论的权限
    COMMENTER =      0b00000100
    #4.管理板块的权限
    BOARDER =        0b00001000
    #5.管理前台用户的权限
    FRONTER =        0b00010000
    #6.管理后台用户的权限
    CMSUSER =        0b00100000

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.ForeignKey('cms_user.id'), primary_key=True)
)

class CmsRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    permission = db.Column(db.Integer, default=CMSPermission.VISITOR)
    desc = db.Column(db.String(100))
    set_time = db.Column(db.DateTime, default=datetime.now)

    users = db.relationship('CmsUser', secondary=cms_role_user, backref='roles')

class CmsUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    set_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permission(self):
        all_permission = 0
        if not self.roles:
            return all_permission
        for role in self.roles:
            permission = role.permission
            all_permission = all_permission|permission
        return all_permission

    def has_permission(self, permission):
        return self.permission&permission == permission

    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)