from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import regexp, length, input_required, equal_to, ValidationError, email
from utils import bbscache

class SignInForm(BaseForm):

    telephone = StringField(validators=[regexp(r'1[345789]\d{9}', message='请输入格式正确的手机号')])
    sms_captcha = StringField(validators=[length(6, 6, message='请输入正确长度的短信验证码')])
    username = StringField(validators=[length(4, -1, message='用户名必须为4位及以上')])
    password1 = StringField(validators=[input_required(message='请输入密码')])
    password2 = StringField(validators=[equal_to('password1', message='两次密码不同')])
    graph_captcha = StringField(validators=[length(4, 4, message='请输入正确长度的图形验证码')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        sms_captcha2 = bbscache.get(self.telephone.data)
        if not sms_captcha2 or sms_captcha.lower() != sms_captcha2.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_graph_captcha(self, filed):
        graph_captcha = filed.data
        graph_captcha2 = bbscache.get(graph_captcha.lower())
        if not graph_captcha2:
            raise ValidationError(message='图形验证码错误')


class LoginForm(BaseForm):
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}', message='请输入格式正确的手机号')])
    password = StringField(validators=[input_required(message='请输入密码')])

    remember_me = IntegerField()


class PostAddForm(BaseForm):
    title = StringField(validators=[input_required('请输入标题')])
    content = StringField(validators=[input_required('请输入内容')])
    board_id = IntegerField(validators=[input_required('请选择所属板块')])


class CommentAddForm(BaseForm):
    content = StringField(validators=[input_required(message='请输入评论内容')])
    post_id = IntegerField(validators=[input_required(message='没有传递帖子ID')])
    reply_to = IntegerField()


class AccountModifyForm(BaseForm):
    username = StringField()
    email = StringField()
    realname = StringField()
    signature = StringField()
    gender = StringField()
    avatar_url = StringField()


class SecurityForm(SignInForm):
    username = StringField()
    old_password = StringField(validators=[input_required('请输入原密码')])

    def validate_password1(self, field):
        password = field.data
        old_password = self.old_password.data
        if password == old_password:
            raise ValidationError('新密码不能和旧密码一致')