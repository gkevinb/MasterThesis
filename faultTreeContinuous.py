from anytree import NodeMixin, RenderTree, LevelOrderIter
import timeseries
import logicgate


# Smarter way to handle distributions as arguments
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

        # Fault tree gate logic is opposite, since it checks for failures not successes
        fault_logic = None
        if self.name == 'AND':
            fault_logic = 'OR'
        if self.name == 'OR':
            fault_logic = 'AND'
        self.parent.time_series = logicgate.evaluate(fault_logic, data_streams)

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

    def get_basic_events(self):
        basic_events = []
        for node in self.root.descendants:
            if node.is_leaf:
                basic_events.append(node)
        return basic_events

    # Maybe make a better way to generate time series for Basic events, probably use inheritance
    def generate_basic_event_time_series(self, size):
        for basic_event in self.get_basic_events():
            basic_event.generate(size)

    def calculate_time_series(self):
        gates = self.get_gates_reversed()
        for gate in gates:
            gate.evaluate()

    def print_tree(self):
        print(RenderTree(self.root))

    def export_time_series(self, file_name):
        file_ext = file_name + '.txt'
        file = open(file_ext, 'w')
        root = self.root
        for times in root.time_series:
            file.write('%s ' % times)
        file.write('\n')
        for basic_event in self.get_basic_events():
            for times in basic_event.time_series:
                file.write('%s ' % times)
            file.write('\n')

        file.close()


# Find way to only allow events to connect with gates and vice versa,
# Event | Gate | Event | Gate | Event layers.
topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
and2 = Gate('AND', parent=intermediateEvent1)
basicEvent1 = Event('Basic Event 1', 'EXP', 10, 'EXP', 4, parent=and2)
basicEvent2 = Event('Basic Event 2', 'EXP', 10, 'EXP', 4, parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent3 = Event('Basic Event 3', 'EXP', 10, 'EXP', 4, parent=or1)
basicEvent4 = Event('Basic Event 4', 'EXP', 10, 'EXP', 4, parent=or1)

fault_tree = FaultTree(topEvent)
# 10000 generation size takes a good minute
fault_tree.generate_basic_event_time_series(100)
fault_tree.calculate_time_series()
fault_tree.print_tree()
fault_tree.export_time_series('testdata2')
