import logging
import os
import time
import torch
from app.retro.utils.common.prepare_utils import prepare_starting_molecules, prepare_mlp, prepare_run_planner

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)


class RSPlanner(object):
    def __init__(self, gpu=0, expansion_topk=50, iterations=3000, viz=False, viz_dir='viz'):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 初始化
        buliding_block_path = os.path.join(BASE_DIR, 'utils/data/iML1515_sinks.csv')
        mlp_templates_path = os.path.join(BASE_DIR, 'utils/data/all_template_rules_1.dat')
        one_step_model_path = os.path.join(BASE_DIR, 'utils/model/one-step-model.ckpt')

        # 用于运算的设备
        device = torch.device('cuda:%d' % gpu if gpu >= 0 and torch.cuda.is_available() else 'cpu')

        # 获取初始模块的starting_mols
        logger.info('--------------start--------------')
        logger.info("Device for prediction: %s" % device)

        # 读取sink
        starting_mols = prepare_starting_molecules(buliding_block_path)
        logger.info("Number of starting mols: %s" % len(starting_mols))
        logger.info("The max iterations is: %s" % iterations)

        # 获取单步预测处理器
        one_step = prepare_mlp(mlp_templates_path, one_step_model_path)

        # 单步预测函数
        one_step_handler = lambda x: one_step.run(x, topk=expansion_topk)

        ''' 定义预测处理器 参数为:单步预测函数 起始sink 迭代次数 viz viz_dir
         return: mol_tree.succ, (best_route, all_routes, best_length, i+1)
         '''
        self.plan_handle = prepare_run_planner(
            expansion_handler=one_step_handler,
            starting_mols=starting_mols,
            iterations=iterations,
            viz=viz,
            viz_dir=viz_dir
        )

    def plan(self, target_mol):
        before_time = time.time()
        logger.info('Running for %s...' % target_mol)
        # 得到的结果是 mol_tree.succ, (best_route, all_routes, best_length, i+1)
        succ, msg = self.plan_handle(target_mol)
        # True or success
        if succ:
            best_route = msg[0].serialize()
            all_routes = msg[1]
            best_length = msg[2]
            excution_time = time.time() - before_time
            iteration = msg[3]
            return best_route, all_routes, best_length, excution_time, iteration

        else:
            logger.info('Synthesis path for %s not found. Please try increasing '
                        'the number of iterations.' % target_mol)
            best_route, all_routes, best_length, excution_time, iteration = '', '', -1, -1, -1
            return best_route, all_routes, best_length, excution_time, iteration


if __name__ == '__main__':
    planner = RSPlanner()
    best_route, all_routes, best_length, excution_time, iteration = planner.plan('OCCCCO')
    print('---------------分数最高的途径---------------')
    print(best_route, best_length, excution_time, iteration)

    for i, route in enumerate(all_routes):
        length = route.length
        route = route.serialize()
        print('---------------途径{}---------------'.format(i + 1))
        print(route, length)

