from anytree import Node, NodeMixin, RenderTree


class Number(NodeMixin):
    def __init__(self, name, n, parent=None):
        self.name = name
        self.num = n
        self.parent = parent

    def __repr__(self):
        return self.name + ' : ' + str(self.num)


udo = Node("Udo")
marc = Node("Marc", parent=udo)
lol = Node("Lol", parent=udo)
jack = Node("Jack", parent=marc)
jill = Node("Jill", parent=marc)

print(RenderTree(udo))
print(udo.children)
n1 = Number("Four", 4)
n2 = Number("Five", 5, parent=n1)
n3 = Number("Six", 6, parent=n1)
n4 = Number("Seven", 7, parent=n2)
n5 = Number("Eight", 8, parent=n2)

'''
# Print out entire tree
for pre, _, node in RenderTree(n1):
    treestr = u"%s%s" % (pre, node.name)
    print(treestr.ljust(7), node.num)
'''
print(udo.descendants)
print(RenderTree(n1))
print(n2.children)
print(n2.path)

L = [10, 20, 30, 40, 50]
print(L)
revL = L[::-1]
print(revL)
print(jill.is_leaf)
print(udo.descendants)
print(len(udo.descendants))
print(len(n1.descendants))
