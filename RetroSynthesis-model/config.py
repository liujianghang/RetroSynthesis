import os.path


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ljh_biod_RetroSynthesis'  # 用来设置session的
    # 项目路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静态文件的路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    # 头像的上传路径
    UPLOAD_ICON_DIR = os.path.join(STATIC_DIR, 'upload/icon')
    # 相册的上传路径
    UPLOAD_PHOTO_DIR = os.path.join(STATIC_DIR, 'upload/photo')
    # WTF图形验证码配置
    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_PRIVATE_KET = ''
    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    # 数据库配置信息
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'retro'
    USERNAME = 'root'
    PASSWORD = 'root'  # root是实验室的mysql密码
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    SQLALCHEMY_DATABASE_URI = DB_URI
    # mysql+pymysql://user:password@hostip:port/databaseName
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qqljhwhg416@127.0.0.1:3306/flask'


class ProductionConfig(Config):
    ENV = 'production'
