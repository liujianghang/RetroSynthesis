from queue import Queue
import logging
import networkx as nx
from copy import deepcopy
from graphviz import Digraph
from .mol_node import MolNode
from .reaction_node import ReactionNode
from .syn_route import SynRoute


class MolTree:
    def  __init__(self, target_mol, known_mols):
        self.target_mol = target_mol
        self.known_mols = known_mols
        self.mol_nodes = []
        self.reaction_nodes = []

        self.root = self._add_mol_node(target_mol, None)
        self.succ = target_mol in known_mols  # 先看target是否就是在sink中

        if self.succ:
            logging.info('Synthesis route found: target in starting molecules')
            # print('Synthesis route found: target in starting molecules')


    def _add_mol_node(self, mol, parent):
        # 添加节点到树且给予序号
        is_known = mol in self.known_mols

        mol_node = MolNode(
            mol=mol,
            parent=parent,
            is_known=is_known
        )
        self.mol_nodes.append(mol_node)
        mol_node.id = len(self.mol_nodes)  # give id

        return mol_node

    def _add_reaction_and_mol_nodes(self, mols, parent, ec_number, template, ancestors):
        for mol in mols:
            if mol in ancestors:
                return

        reaction_node = ReactionNode(
            parent=parent,
            ec_number=ec_number,
            template=template
        )
        for mol in mols:
            self._add_mol_node(mol, reaction_node)
        reaction_node.init_succ()  # 初始化
        self.reaction_nodes.append(reaction_node)
        reaction_node.id = len(self.reaction_nodes) # 添加序号

        return reaction_node

    def expand(self, mol_node, reactant_lists, ec_numbers, templates):
        #
        assert not mol_node.is_known and not mol_node.children

        if reactant_lists is None:      # No expansion results
            if mol_node.parent:
                mol_node.parent.backup(from_mol=mol_node.mol)
            return self.succ

        assert mol_node.open
        ancestors = mol_node.get_ancestors()
        for i in range(len(reactant_lists)):
            self._add_reaction_and_mol_nodes(reactant_lists[i], mol_node, ec_numbers[i], templates[i], ancestors)

        if len(mol_node.children) == 0:      # No valid expansion results
            if mol_node.parent:
                mol_node.parent.backup(from_mol=mol_node.mol)
            return self.succ
        
        mol_node.init_succ()
        if mol_node.parent:
            mol_node.parent.backup(from_mol=mol_node.mol)

        if not self.succ and self.root.succ:
            logging.info('Synthesis route found!')
            self.succ = True

        return self.succ

    def get_best_route(self):
        if not self.succ:
            return None

        syn_route = SynRoute(
            target_mol=self.root.mol
        )

        mol_queue = Queue()
        mol_queue.put(self.root)

        while not mol_queue.empty():
            mol = mol_queue.get()
            if mol.is_known:
                continue

            best_reaction = None
            for reaction in mol.children:
                if reaction.succ:
                    if best_reaction is None:
                        best_reaction = reaction

            reactants = []
            for reactant in best_reaction.children:
                mol_queue.put(reactant)
                reactants.append(reactant.mol)

            syn_route.add_reaction(
                mol=mol.mol,
                ec_number=best_reaction.ec_number,
                template=best_reaction.template,
                reactants=reactants
            )

        return syn_route

    def get_routes(self):
        if not self.succ:
            return None

        routes = []
        syn_route = SynRoute(
            target_mol=self.root.mol
        )
        routes.append(syn_route)

        mol_queue = Queue()
        mol_queue.put((syn_route, self.root))
        while not mol_queue.empty():
            syn_route, mol = mol_queue.get()
            if mol.is_known:
                continue

            best_reaction = None
            all_reactions = []
            for reaction in mol.children:
                if reaction.succ:
                    all_reactions.append(reaction)
                    if best_reaction is None:
                        best_reaction = reaction
            # assert best_reaction.succ_value == mol.succ_value

            syn_route_template = None
            if len(all_reactions) > 1:
                syn_route_template = deepcopy(syn_route)

            # best reaction
            reactants = []
            for reactant in best_reaction.children:
                mol_queue.put((syn_route, reactant))
                reactants.append(reactant.mol)

            syn_route.add_reaction(
                mol=mol.mol,
                ec_number=best_reaction.ec_number,
                template=best_reaction.template,
                reactants=reactants
            )

            # other reactions
            if len(all_reactions) > 1:
                for reaction in all_reactions:
                    if reaction == best_reaction:
                        continue

                    syn_route = deepcopy(syn_route_template)
                    routes.append(syn_route)

                    reactants = []
                    for reactant in reaction.children:
                        mol_queue.put((syn_route, reactant))
                        reactants.append(reactant.mol)

                    syn_route.add_reaction(
                        mol=mol.mol,
                        ec_number=reaction.ec_number,
                        template=reaction.template,
                        reactants=reactants
                    )

        return routes
    
    def viz_search_tree(self, viz_file):
        G = Digraph('G', filename=viz_file)
        G.attr(rankdir='LR')
        G.attr('node', shape='box')
        G.format = 'pdf'

        node_queue = Queue()
        node_queue.put((self.root, None))
        while not node_queue.empty():
            node, parent = node_queue.get()

            if node.open:
                color = 'lightgrey'
            else:
                color = 'aquamarine'

            if hasattr(node, 'mol'):
                shape = 'box'
            else:
                shape = 'rarrow'

            if node.succ:
                color = 'lightblue'
                if hasattr(node, 'mol') and node.is_known:
                    color = 'lightyellow'

            G.node(node.serialize(), shape=shape, color=color, style='filled')

            label = ''
            if hasattr(parent, 'mol'):
                label = '%s' % (node.children.ec_number)
            if parent is not None:
                G.edge(parent.serialize(), node.serialize(), label=label)

            if node.children is not None:
                for c in node.children:
                    node_queue.put((c, node))

        G.render()