class ReactionNode:
    def __init__(self, parent, ec_number, template):
        self.parent = parent
        
        self.depth = self.parent.depth + 1
        self.id = -1
        self.ec_number = ec_number
        self.template = template
        self.children = []
        self.succ = None    # successfully found a valid synthesis route
        self.open = True    # before expansion: True, after expansion: False
        parent.children.append(self)

    def init_succ(self):
        assert self.open

        self.succ = True
        for mol in self.children:
            self.succ &= mol.succ

        self.open = False
        
    def backup(self, from_mol=None):
        self.succ = True
        for mol in self.children:
            self.succ &= mol.succ
            
        return self.parent.backup(self.succ)

    def serialize(self):
        return '%d' % (self.id)
