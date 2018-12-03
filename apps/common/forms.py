from ..forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import regexp, input_required, length, equal_to, ValidationError
import hashlib
from utils import bbscache

class SMSCaptchaForm(BaseForm):

    salt = 'as43&%HUGgygTFYVcdse2'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[input_required()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        sign2 = hashlib.md5((telephone + timestamp + self.salt).encode()).hexdigest()
        if sign == sign2:
            return True
        else:
            return False



