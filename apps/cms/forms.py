from wtforms import StringField, IntegerField
from wtforms.validators import email, input_required, equal_to, ValidationError
from ..forms import BaseForm
from utils import bbscache
from flask import g


class LoginFrom(BaseForm):
    email = StringField(validators=[email(message='请输入正确的邮箱地址'), input_required(message='请输入邮箱')])
    password = StringField(validators=[input_required(message='请输入密码')])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    old_password = StringField(validators=[input_required(message='请输入原密码')])
    new_password = StringField(validators=[input_required(message='请输入新密码')])
    new_password_repeat = StringField(validators=[equal_to('new_password', message='两次密码不一致')])


class ResetemailForm(BaseForm):
    email = StringField(validators=[email(message='请输入正确格式的邮箱’')])
    captcha = StringField(validators=[input_required(message='请输入验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha2 = bbscache.get(email)
        if not captcha2 or captcha.lower() != captcha2.lower():
            raise ValidationError('验证码不一致')

    def validate_email(self, field):
        email = field.data
        if email == g.cms_user.email:
            raise ValidationError('不能修改为相同的邮箱')


class BannerForm(BaseForm):
    name = StringField(validators=[input_required('请输入轮播图名称')])
    image_url = StringField(validators=[input_required('请输入图片链接')])
    link_url = StringField(validators=[input_required('请输入跳转链接')])
    priority = IntegerField()


class UpdataBannerForm(BannerForm):
    banner_id = IntegerField(validators=[input_required(message='id传递失败')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[input_required(message='请输入板块名称')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[input_required(message='没有提供板块ID')])
