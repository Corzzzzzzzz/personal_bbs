from flask import Blueprint, jsonify, make_response, request
from utils import bbscache, restful
from utils.captcha import Captcha
from utils.aliyunsdk.aliyunsms import send_sms
from io import BytesIO
import qiniu
from .forms import SMSCaptchaForm
import random, json


bp = Blueprint('common', __name__, url_prefix='/common')


@bp.route('/')
def index():
    return 'common page'


@bp.route('/upload_qiniu/', methods=["GET", "POST"])
def upload_qiniu():
    access_key = 'SJzKzuxsqx4XPIZ44cfVmDJncqqX2HwaDkxT93tp'
    secret_key = 'AkmSBkAP_C1wEz8krwA5xfeDqN4R1gkWnfx5QqQZ'
    q = qiniu.Auth(access_key, secret_key)
    bucket = 'corz-cache'
    token = q.upload_token(bucket)
    return jsonify({"uptoken": token})


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    bbscache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        code = ''.join(random.sample([str(i) for i in range(10)], 6))
        result = send_sms(telephone, code)
        result = json.loads(result.decode())
        if result['Message'] == 'OK':
            bbscache.set(telephone, code, timeout=300)
            print('验证码：', code)
            return restful.success()
        else:
            return restful.params_error(message=result['Message'])
    else:
        return restful.params_error(message='参数错误')