from flask import Flask
from app.retro.view import retro_bp
from app.user.view import user_bp
from exts import cors, db
import config


def create_app():
    app = Flask(__name__, static_folder='retro')  # 默认是找同级的文件夹，这里一定要调整
    # 加载app配置文件
    app.config.from_object(config.DevelopmentConfig)
    # 插件初始化
    db.init_app(app=app)
    cors.init_app(app=app, supports_credentials=True)
    app.register_blueprint(retro_bp)
    app.register_blueprint(user_bp)
    return app
