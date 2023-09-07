import os

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG
import pubchempy as pcp
from app.retro.RSPlanner.RSPlanner import RSPlanner

# 该模块用于数据的处理
# 定义svg绘制路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
draw_path = os.path.join(BASE_DIR, 'tmp/svg')


def plan(target_mol, expansion_topk, iterations):
    global mols
    model = RSPlanner(expansion_topk=expansion_topk, iterations=iterations)
    """
        用以预测单个分子
        Parameters
        ----------
        target_mol

        Returns
        -------
        result:[
        "best_route","best_length","excution_time","iteration","all_routes"
        ]

        """

    best_route, all_routes, best_length, excution_time, iteration = model.plan(target_mol)
    if best_route == '':
        return ''
    result = {'target_mol': target_mol,
              'best_route': best_route,
              'best_length': best_length,
              'excution_time': excution_time,
              'iteration': iteration,
              'expansion_topk': expansion_topk}
    # 序列化routes
    routes = []
    for i, route in enumerate(all_routes):
        routes.append(route.serialize())
    result['all_routes'] = routes
    # 获取元素和映射,最好的路线的edge,build block
    result['elements'], result['r_map'] = getNodesAndEdges(routes)
    result['best_edges'] = getBestRouteEdge(best_route)
    result['build_blocks'] = getBuildBlocks(routes)
    result['cid'] = pcp.get_cids(target_mol, 'smiles')[0]
    # 绘制部分(svg)
    if not os.path.exists(draw_path):
        os.makedirs(draw_path)
    if result['elements'][0]:
        mols = result['elements'][0]  # 获取所有的分子
        drawSVG(mols)
        result['cids'] = getCids(mols)
        result['isSuccess'] = True
    else:
        result['cids'] = {}
        result['isSuccess'] = False

    # print(result)
    return result


def getNodesAndEdges(routes):
    """
    用以获取路径的节点和边

    Parameters
    ----------
    routes

    Returns
    -------

    """
    node_m = set()
    node_r = set()
    edges = set()
    # 让反应物变成唯一标识
    single_set = set()
    # 让reaction产生映射的map
    count_r = 1
    r_map = {}
    elements = []
    try:
        for route in routes:
            for route_single in route.split('|'):  # 获取单步反应
                if route_single not in single_set:
                    # 加入到单步反应的集合中
                    single_set.add(route_single)
                    tmp = route_single.split('>')  # 获取单步反应中的产物，反应酶，反应物
                    source = tmp[0]
                    reaction = tmp[1]
                    # 产生映射
                    r_key = 'r' + str(count_r)  # key
                    count_r += 1  # count_r自增
                    # 写入映射
                    r_map[r_key] = reaction
                    target = tmp[2]
                    node_m.add(source)
                    node_r.add(r_key)
                    for r in target.split('.'):
                        node_m.add(r)
                        edges.add(source + '>>' + r_key)
                        edges.add(r_key + '>>' + r)
                else:
                    pass
        elements.append(list(node_m))
        elements.append(list(node_r))
        elements.append(list(edges))
    except Exception as e:
        return [[], [], []], {}
    return elements, r_map


def getBestRouteEdge(best_route):
    best_edges = set()
    r_map = {}
    count_r = 1
    try:
        for route_single in best_route.split('|'):  # 获取单步反应
            tmp = route_single.split('>')  # 获取单步反应中的产物，反应酶，反应物
            source = tmp[0]
            reaction = tmp[1]
            # 产生映射
            r_key = 'r' + str(count_r)  # key
            count_r += 1  # count_r自增
            target = tmp[2]
            for r in target.split('.'):
                best_edges.add(source + '>>' + r_key)
                best_edges.add(r_key + '>>' + r)
    except Exception as e:
        return []
    return list(best_edges)


def drawSVG(mols, molSize=(300, 300)):
    """
    用以根据节点集合绘制相应的SVG矢量图
    Parameters
    ----------
    mols
    molSize
    """
    for mol in mols:
        diclofenac = Chem.MolFromSmiles(mol)
        d2d = rdMolDraw2D.MolDraw2DSVG(molSize[0], molSize[1])
        d2d.DrawMolecule(diclofenac)
        d2d.FinishDrawing()
        SVG(d2d.GetDrawingText())
        with open(f'app/retro/tmp/svg/{mol}.svg', 'w+') as result:
            result.write(d2d.GetDrawingText())


def getCids(mols, namespace='smiles'):
    mol_cid = {}
    for mol in mols:
        cid = pcp.get_cids(mol, namespace)
        mol_cid[mol] = cid[0]
    return mol_cid


def getBuildBlocks(routes):
    build_block = []
    for route in routes:
        tmp = route.split('>')
        for b in tmp[-1].split('.'):
            build_block.append(b)
    return build_block


if __name__ == '__main__':
    # mols = 'CCC(=O)O'
    # mol_cid = {}
    # results = pcp.get_cids(mols, 'smiles')
    # c = pcp.Compound.from_cid(743)
    # print(c.isomeric_smiles)
    # result =
    # a =
    result = getBuildBlocks([
        "[NH]1CCCC1>0>C1=NCCC1|C1=NCCC1>2.6.1.82>NCCCCN",
        "[NH]1CCCC1>0>C1=NCCC1|C1=NCCC1>1.5.1>NCCCC(=O)O",
        "[NH]1CCCC1>0>C1=NCCC1|C1=NCCC1>1.5.99.6>NCCCCNCCCN",
        "[NH]1CCCC1>0>C1=NCCC1|C1=NCCC1>2.6.1.82>NCCCC=O"
    ])
    print(result)
