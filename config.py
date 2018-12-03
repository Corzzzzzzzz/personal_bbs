
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Reborn@@cjb@localhost:3306/bbs?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'add salt'

CMS_USER_ID = 'cms_user_id'
USER_ID = 'user_id'

#email config
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = '1372756176@qq.com'
MAIL_PASSWORD = 'ccugqsenqgoxfeic'
MAIL_DEFAULT_SENDER = '1372756176@qq.com'


# UEditor的相关配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "SJzKzuxsqx4XPIZ44cfVmDJncqqX2HwaDkxT93tp"
UEDITOR_QINIU_SECRET_KEY = "AkmSBkAP_C1wEz8krwA5xfeDqN4R1gkWnfx5QqQZ"
UEDITOR_QINIU_BUCKET_NAME = "corz-cache"
UEDITOR_QINIU_DOMAIN = "http://7xqenu.com1.z0.glb.clouddn.com/"

#flask paginate的相关配置
PER_PAGE = 10