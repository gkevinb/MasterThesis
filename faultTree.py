from anytree import NodeMixin, RenderTree, LevelOrderIter


class Event(NodeMixin):
    def __init__(self, name, reliability=None, failure_rate=None, parent=None):
        self.name = name
        self.reliability = reliability
        if reliability is None:
            self.probability = reliability
        else:
            self.probability = (1 - reliability)
        self.failureRate = failure_rate
        self.parent = parent

    def __repr__(self):
        return self.name + ' : ' + str(self.reliability) + ' : ' + str(self.probability) \
               + ' : ' + str(self.reliability + self.probability)


class Gate(NodeMixin):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def children_have_reliability(self):
        check = True
        for child in self.children:
            if child.reliability is None:
                check = False
                break
        return check

    def children_have_probability(self):
        check = True
        for child in self.children:
            if child.probability is None:
                check = False
                break
        return check

    def evaluate_rel(self):
        if self.children_have_reliability():
            reliabilities = 1
            if self.name == 'AND':
                for child in self.children:
                    reliabilities *= (1 - child.reliability)
                self.parent.reliability = 1 - reliabilities
            if self.name == 'OR':
                for child in self.children:
                    reliabilities *= child.reliability
                self.parent.reliability = reliabilities

    def evaluate_prob(self):
        if self.children_have_probability():
            probabilities = 1
            if self.name == 'AND':
                for child in self.children:
                    probabilities *= child.probability
                self.parent.probability = probabilities
            if self.name == 'OR':
                for child in self.children:
                    probabilities *= (1 - child.probability)
                self.parent.probability = 1 - probabilities

    def __repr__(self):
        return self.name


class FaultTree:
    def __init__(self, root):
        self.root = root

    def calculate_reliability(self):
        gates = []
        for node in LevelOrderIter(self.root):
            if type(node) is Gate:
                gates.append(node)
        gates_reversed = gates[::-1]
        for gate in gates_reversed:
            gate.evaluate_rel()

    def calculate_probability(self):
        gates = []
        for node in LevelOrderIter(self.root):
            if type(node) is Gate:
                gates.append(node)
        gates_reversed = gates[::-1]
        for gate in gates_reversed:
            gate.evaluate_prob()

    def print_tree(self):
        print(RenderTree(self.root))


# Works Best for Binary Tree, each gate only has two branches
topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intEvent1 = Event('Intermediate Event 1', parent=and1)
intEvent2 = Event('Intermediate Event 2', parent=and1)
or1 = Gate('OR', parent=intEvent1)
and2 = Gate('AND', parent=intEvent2)
basicEvent1 = Event('Basic Event 1', 0.23, parent=or1)
basicEvent2 = Event('Basic Event 2', 0.69, parent=or1)

basicEvent3 = Event('Basic Event 3', 0.85, parent=and2)
basicEvent4 = Event('Basic Event 4', 0.98, parent=and2)
basicEvent5 = Event('Basic Event 5', 0.94, parent=and2)
basicEvent6 = Event('Basic Event 6', 0.83, parent=and2)

'''
Example 11. from Reliability PDF
'''
boosterRocket = Event('Booster Rocket Failure')
andBooster = Gate('AND', parent=boosterRocket)
oRing1 = Event('O-ring 1', 0.95, parent=andBooster)
oRing2 = Event('O-ring 2', 0.95, parent=andBooster)


fault_tree = FaultTree(topEvent)
fault_tree.calculate_reliability()
fault_tree.calculate_probability()
fault_tree.print_tree()
