from datetime import datetime

from exts import db


class Molecule(db.Model):
    # 目标分子信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mol = db.Column(db.String(64), unique=True, nullable=False)
    iteration = db.Column(db.Integer)
    expansionTopk = db.Column(db.Integer)
    excutionTime = db.Column(db.Float)

    # 查询所得到的基本信息
    cid = db.Column(db.Integer)
    bestRoute = db.Column(db.String(512))
    bestLength = db.Column(db.Integer)

    # 创建时间
    createTime = db.Column(db.DateTime, default=datetime.now)

    # 反向引用
    routes = db.relationship('Route', backref=db.backref('molecule'))


class User_Molecule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    molecule_id = db.Column(db.Integer, db.ForeignKey('molecule.id'))
    isSuccess = db.Column(db.Boolean, nullable=False)


class Route(db.Model):
    # 路径信息
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route = db.Column(db.String(512), unique=True, nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.now)
    # 外键
    moleculeId = db.Column(db.Integer, db.ForeignKey('molecule.id'))
