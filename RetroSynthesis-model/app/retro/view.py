from flask import Blueprint, request, jsonify
from exts import db

from app.retro.RSPlanner import plan
from app.retro.models import Molecule, User_Molecule, Route
from app.user.models import User

retro_bp = Blueprint('retro', __name__, url_prefix='/api/retro')


@retro_bp.route("/test")
def test():
    return "ok"


@retro_bp.route('/plan', methods=['GET', "POST"])
def predict():
    """
    该视图函数用来实现单个目标分子合成路径的预测
    :return: 结果中包含：{全部的合成路径，最佳路径，最佳路径长度，执行时间，迭代次数}
    """

    data = request.get_json()
    target_mol = str(data['target_mol'])
    target_iterations = int(data['target_iterations'])
    target_expansion_topk = int(data['expansion_topk'])
    # username = str(data['username'])
    result = plan.plan(target_mol, target_expansion_topk, target_iterations)

    # # 如果失败
    # if result == '':
    #     return jsonify({'status': 404, 'msg': 'wrong'})
    # elif result['target_mol'] == result['best_route']:
    #     return jsonify({'status': 404, 'msg': 'basic'})
    # elif result['best_length'] == 0:
    #     return jsonify({'status': 404, 'msg': 'fail'})
    #
    # # 如果成功，添加一个成功的状态码
    # result['status'] = 200
    #
    # # 加入到数据库
    # user_select = User.query.filter(User.username == username).first()
    # if user_select:
    #     molecule = Molecule()
    #     molecule.mol = result['target_mol']
    #     molecule.iteration = result['iteration']
    #     molecule.expansionTopk = result['expansion_topk']
    #     molecule.excutionTime = result['excution_time']
    #     molecule.cid = result['cid']
    #     molecule.bestRoute = result['best_route']
    #     molecule.bestLength = result['best_length']
    #     db.session.add(molecule)
    #     db.session.commit()
    #     ##
    #     mol_select = Molecule.query.filter(Molecule.mol == molecule.mol).first()
    #     if mol_select:
    #         user_molecule = User_Molecule()
    #         user_molecule.user_id = user_select.id
    #         user_molecule.molecule_id = mol_select.id
    #         user_molecule.isSuccess = result['isSuccess']
    #         # 提交联系
    #         db.session.add(user_molecule)  # 缓存
    #         routes = result['all_routes']
    #         for r in routes:
    #             route = Route()
    #             route.route = r
    #             route.moleculeId = mol_select.id
    #             db.session.add(route)
        # db.session.commit()
    # 返回结果
    return jsonify(result)
