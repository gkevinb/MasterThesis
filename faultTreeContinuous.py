from anytree import NodeMixin, RenderTree, LevelOrderIter
import timeseries
import logicgate


class Event(NodeMixin):
    def __init__(self, name, reliability_distribution=None, mean_time_to_failure=None,
                 maintainability_distribution=None, mean_time_to_repair=None, parent=None):
        self.name = name
        self.reliability_distribution = reliability_distribution
        self.maintainability_distribution = maintainability_distribution
        self.mean_time_to_failure = mean_time_to_failure
        self.mean_time_to_repair = mean_time_to_repair
        self.parent = parent
        self.time_series = []

    def __repr__(self):
        return self.name + ' : ' + str(self.time_series)

    # Size right now generates a time series 2 x size, since generates both failure times and repair times
    def generate(self, size):
        self.time_series = timeseries.generate_time_series(self.reliability_distribution,
                                                           self.mean_time_to_failure,
                                                           self.maintainability_distribution,
                                                           self.mean_time_to_repair,
                                                           size)


class Gate(NodeMixin):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def evaluate(self):
        data_streams = []
        for child in self.children:
            data_streams.append(child.time_series)
        self.parent.time_series = logicgate.evaluate(self.name, data_streams)

    def __repr__(self):
        return self.name


class FaultTree:
    def __init__(self, root):
        self.root = root

    def get_gates_reversed(self):
        gates = []
        for node in LevelOrderIter(self.root):
            if type(node) is Gate:
                gates.append(node)
        return gates[::-1]

    def generate_basic_event_time_series(self, size):
        for node in self.root.descendants:
            if node.is_leaf:
                node.generate(size)

    def calculate_time_series(self):
        gates = self.get_gates_reversed()
        for gate in gates:
            gate.evaluate()

    def print_tree(self):
        print(RenderTree(self.root))


topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
basicEvent1 = Event('Basic Event 1', 'EXP', 10, 'EXP', 4, parent=and1)
basicEvent2 = Event('Basic Event 2', 'EXP', 10, 'EXP', 4, parent=and1)


fault_tree = FaultTree(topEvent)
fault_tree.generate_basic_event_time_series(100)
fault_tree.calculate_time_series()
fault_tree.print_tree()
