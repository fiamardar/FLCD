class Node:
    index = None
    info = None
    parent = None
    sibling = None

    def __init__(self, index, info, parent, sibling):
        self.index = index
        self.info = info
        self.parent = parent
        self.sibling = sibling

    def get_parent(self):
        return self.parent

    def get_info(self):
        return self.info
