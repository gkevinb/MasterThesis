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

    def generate(self, size):
        """
        Generate time series based on distribution of events.
        :param size: Size of time series to generate; Size right now generates a time series 2 x size,
        since generates both failure times and repair times.
        :return:
        """
        self.time_series = timeseries.generate_time_series(self.reliability_distribution,
                                                           self.mean_time_to_failure,
                                                           self.maintainability_distribution,
                                                           self.mean_time_to_repair,
                                                           size)

    def __repr__(self):
        return self.name + ' : ' + str(self.time_series)


class Gate(NodeMixin):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def evaluate(self):
        """
        Evaluate the gate inputs and modify the gate output. Based on the gate type and gate input time series,
        calculate time series for gate output.
        Note: Fault tree gate logic is opposite, since it checks for failures not successes.
        :return:
        """
        data_streams = []
        for child in self.children:
            data_streams.append(child.time_series)

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

    def _get_gates_reversed(self):
        """
        Get the reverse order of the gates so it starts from the lower level gates and goes to the higher level gates.
        :return: List of gates ordered from the lower level to the higher level.
        """
        gates = []
        for node in LevelOrderIter(self.root):
            if type(node) is Gate:
                gates.append(node)
        return gates[::-1]

    def _get_basic_events(self):
        """
        Get basic events from Fault Tree Structure
        :return: Basic events
        """
        basic_events = []
        for node in self.root.descendants:
            if node.is_leaf:
                basic_events.append(node)
        return basic_events

    # Maybe make a better way to generate time series for Basic events, probably use inheritance, probably don't
    # need to!!!!!
    def generate_basic_event_time_series(self, size):
        """
        Generate time series for basic events.
        :param size: Size of generated time series.
        :return:
        """
        for basic_event in self._get_basic_events():
            basic_event.generate(size)

    def calculate_time_series(self):
        """
        Calculate time series of all events except basic events.
        :return:
        """
        gates = self._get_gates_reversed()
        for gate in gates:
            gate.evaluate()

    def print_tree(self):
        """
        Render the tree in the console.
        :return:
        """
        print(RenderTree(self.root))

    def export_time_series(self, file_name):
        """
        Export time series into a txt file with file_name as the name.
        :param file_name: Name of the file without extension
        :return:
        """
        file_ext = file_name + '.txt'
        file = open(file_ext, 'w')
        root = self.root
        for times in root.time_series:
            file.write('%s ' % times)
        file.write('\n')
        for basic_event in self._get_basic_events():
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
