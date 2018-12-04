from exts import db
from datetime import datetime


class BannerModel(db.Model):
    __tablename__ = 'banner'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


like_relation = db.Table(
    'like_relation',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('user_id', db.String(100), db.ForeignKey('front_user.id'),primary_key=True)
)


class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'), nullable=False)

    board = db.relationship('BoardModel', backref='posts')
    author = db.relationship('FrontUser', backref='posts')
    likers = db.relationship('FrontUser', secondary=like_relation, backref='liking_posts')

    def check_liker(self, user):
        if user in self.likers:
            return True
        else:
            return False


class HighlightPost(db.Model):
    __tablename__ = 'highlight_post'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('PostModel', backref='highlight')


# class LikePost(db.Model):
#     __tablename__ = 'like_post'
#
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
#     user_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
#
#     post = db.relationship('PostModel', backref='likes')
#     user = db.relationship('FrontUser', backref='likes')


class CommentModel(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    commenter_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))

    post = db.relationship('PostModel', backref='comments')
    commenter = db.relationship('FrontUser', backref='comments')






