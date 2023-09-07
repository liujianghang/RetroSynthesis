'''
 原因：出现导入文件标红的问题，是因为文件目录设置的问题，pycharm中的最上层文件夹是项目文件夹，在项目中导包默认是从这个目录下寻找，当在其中再次建立目录，
 目录内的py文件如果要导入当前目录内的其他文件，单纯的使用import导入，是得不到智能提示的，这是pycharm设置的问题，并非导入错误。
'''

from flask_script import Manager
# flask_migrate的第十五行改一下 from flask_script._compat import text_type
from flask_migrate import Migrate, MigrateCommand  # 特别注意版本为2.7.0
from app import create_app
from app.user.models import User  # 这是必须的
from app.retro.models import *  # 这是必须的
from exts import db

# CCC(=O)O
# 应用工程模式创建
app = create_app()


# 测试
@app.route('/')
def hello():
    return 'hello'


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 脚本形式启动
manager.run()  # python app.py runserver -h 0.0.0.0 -p 5001

# 数据库命令
# python app.py db init 生成库
# python app.py db migrate 生成文件
# python app.py db upgrade 执行文件中的upgrade
