from queue import Queue
from graphviz import Digraph # 有向图

class SynRoute:
    def __init__(self, target_mol):
        self.target_mol = target_mol  # assum target idx = 0
        self.mols = [target_mol]
        self.ec_numbers = [None]
        self.templates = [None]
        self.parents = [-1]
        self.children = [None]
        self.length = 0

    def _add_mol(self, mol, parent_id):
        self.mols.append(mol)
        self.ec_numbers.append(None)
        self.templates.append(None)
        self.parents.append(parent_id)
        self.children.append(None)

        self.children[parent_id].append(len(self.mols)-1)

    def add_reaction(self, mol, ec_number, template, reactants):
        assert mol in self.mols

        self.length += 1

        parent_id = self.mols.index(mol)
        self.ec_numbers[parent_id] = ec_number
        self.templates[parent_id] = template
        self.children[parent_id] = []

        for reactant in reactants:
            self._add_mol(reactant, parent_id) # children[0] = [1,2]

    def viz_route(self, viz_file):
        G = Digraph('G', filename=viz_file)
        G.attr('node', shape='box')
        G.format = 'pdf'

        # get all mol's name
        names = []
        for i in range(len(self.mols)):
            name = self.mols[i]
            # if self.templates[i] is not None:
            #     name += ' | %s' % self.templates[i]
            names.append(name)

        node_queue = Queue()
        node_queue.put((0,-1))   # target mol idx, and parent idx
        while not node_queue.empty():
            idx, parent_idx = node_queue.get()

            if parent_idx >= 0:
                G.edge(names[parent_idx], names[idx], label='enzyme')

            if self.children[idx] is not None: # 如果是存了孩子的
                for c in self.children[idx]:
                    node_queue.put((c, idx))

        G.render()

    def serialize_reaction(self, idx):
        # 链接单个reaction节点
        s = self.mols[idx]
        if self.children[idx] is None:
            return s
        s += '>%s>' % self.ec_numbers[idx]
        s += self.mols[self.children[idx][0]]
        for i in range(1, len(self.children[idx])):
            s += '.'
            s += self.mols[self.children[idx][i]]

        return s

    def serialize(self):
        # 链接全路径
        s = self.serialize_reaction(0)
        for i in range(1, len(self.mols)):
            if self.children[i] is not None:
                s += '|'
                s += self.serialize_reaction(i)
        return s