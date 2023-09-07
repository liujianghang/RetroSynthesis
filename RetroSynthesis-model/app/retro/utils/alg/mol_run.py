import logging
from .mol_tree import MolTree

# 多步
def mol_run(target_mol, target_mol_id, starting_mols, expand_fn, iterations, viz=False, viz_dir=None):
    mol_tree = MolTree(
        target_mol=target_mol,
        known_mols=starting_mols
    )

    i = -1

    if not mol_tree.succ:
        for i in range(iterations):
            if(i <= len(mol_tree.mol_nodes)-1):
                m_next = mol_tree.mol_nodes[i] # 对序列中每一个都进行拓展

                if m_next.open:
                    result = expand_fn(m_next.mol) # 对这个节点进行单步预测
                else:
                    continue

                if result is not None and (len(result['reactants']) > 0):
                    reactants = result['reactants']
                    ec_numbers = result['enzymes']
                    templates = result['templates']

                    reactant_lists = []  # 重新对反应物划分
                    for j in range(len(reactants)):
                        reactant_list = list(set(reactants[j].split('.')))
                        reactant_lists.append(reactant_list)

                    assert m_next.open
                    succ = mol_tree.expand(m_next, reactant_lists, ec_numbers, templates)

                    if succ:  # 如果不是sink则succ
                        break

                else: # 单步预测失败
                    mol_tree.expand(m_next, None, None, None)
                    logging.info('Expansion fails on %s! in iter %d' % (m_next.mol, i+1))
            else:
                logging.info('No nodes available for expansion')
                break
                
    best_route = None
    all_routes = None
    best_length = 0
    
    if mol_tree.succ:
        best_route = mol_tree.get_best_route()
        all_routes = mol_tree.get_routes()
        all_routes = sorted(all_routes, key=lambda x: x.length)
        best_length = best_route.length

    return mol_tree.succ, (best_route, all_routes, best_length, i+1)