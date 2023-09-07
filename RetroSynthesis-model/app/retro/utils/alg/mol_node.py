class MolNode:
    def __init__(self, mol, parent=None, is_known=False):
        self.mol = mol
        self.parent = parent

        self.id = -1
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth

        self.is_known = is_known
        self.children = []
        self.succ = is_known  # 该分子起始能否被拓展取决于是否是inSink 如果是 则该节点是succ性质的
        self.open = True    # before expansion: True, after expansion: False
        if is_known:
            self.open = False
            
        if parent is not None:
            parent.children.append(self)

    def init_succ(self):
        # 确保该分子节点未被扩展(因为assert open为true,则该节点一定不为sink)
        assert self.open
        # assert self.open and (no_child or self.children)

        # 或
        self.succ = False
        for reaction in self.children:
            self.succ |= reaction.succ
            
        # 扩展完毕后 标记为被扩展
        self.open = False
        
    def backup(self, succ):
        # 确定该分子节点不是sink
        assert not self.is_known

        # 更新该节点是否可行
        new_succ = self.succ | succ
        updated = (self.succ != new_succ)
        self.succ = new_succ
        # 如果该节点被更新过且有父reaction节点 则继续迭代到上层的reaction
        if updated and self.parent:
            return self.parent.backup(from_mol=self.mol)


    def get_ancestors(self):
        # 获得该分子节点的所有父node节点
        if self.parent is None:
            return {self.mol}

        ancestors = self.parent.parent.get_ancestors()
        ancestors.add(self.mol)
        return ancestors
