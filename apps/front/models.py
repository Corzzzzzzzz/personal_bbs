from exts import db
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class Follow(db.Model):
    __tablename__ = 'follow'

    follower_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), primary_key=True)
    followed_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), primary_key=True)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class FrontUser(db.Model):
    __tablename__ = 'front_user'

    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(40))
    realname = db.Column(db.String(20))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)

    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
        super(FrontUser, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpw):
        self._password = generate_password_hash(newpw)

    def check_password(self, rawpw):
        return check_password_hash(self.password, rawpw)

    def is_following(self, user):
        if user.id is None:
            return False
        else:
            return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        else:
            return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
