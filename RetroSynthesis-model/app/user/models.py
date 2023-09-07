from datetime import datetime

from exts import db


# 在将models中的字段的db.String(256)修改为db.String(1024)后，执行migrate和upgrade操作后，发现数据库并没有更新，网上查阅资料后，解决方法如下：
# 打开env.py文件（文件路径为：migrations/env.py）
# 找到run_migrations_online函数下的context.configure,在括号中添加两行配置项
# compare_type=True,
# compare_server_default=True
# 添加完成后再次迁移即可成功

# 必须要继承才是可以完成ORM映射的类
class User(db.Model):
    # db.Column(类型，约束) 映射表中的类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(32))
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean, default=False)  # 逻辑删除
    registerTime = db.Column(db.DateTime, default=datetime.now)

    # 增加一个字段, 建立两张表之间有外键 关系
    molecules = db.relationship('Molecule', backref='user', secondary='user__molecule')

    def __str__(self):
        return self.username
