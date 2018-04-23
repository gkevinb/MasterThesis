from anytree import NodeMixin, RenderTree, LevelOrderIter
from modules import logicgate, timeseries
from analyzeData import TimeSeries

DISPLAY_UP_TO = 6


# Smarter way to handle distributions as arguments
class Event(NodeMixin):
    def __init__(self, name, reliability_distribution=None, maintainability_distribution=None, parent=None):
        self.name = name
        self.reliability_distribution = reliability_distribution
        self.maintainability_distribution = maintainability_distribution
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
                                                           self.maintainability_distribution,
                                                           size)

    def __repr__(self):
        # return self.name + ' : ' + str(self.time_series[:DISPLAY_UP_TO])
        # MAKE THIS BETTER LATER!!!!!!!!
        return self.name + ' : ' + str(self.reliability_distribution)


class Gate(NodeMixin):
    def __init__(self, name, parent=None, k=None):
        self.name = name
        self.parent = parent
        self.k = k

    def get_number_of_children(self):
        return len(self.children)

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
        if self.name == 'VOTING':
            fault_logic = self.k

        self.parent.time_series = logicgate.evaluate(fault_logic, data_streams)

    def __repr__(self):
        if self.k is None:
            return self.name
        else:
            return str(self.k) + '/' + str(self.get_number_of_children()) + ' ' + self.name


class FaultTree:
    def __init__(self, top_event):
        self.top_event = top_event

    def _get_gates_reversed(self):
        """
        Get the reverse order of the gates so it starts from the lower level gates and goes to the higher level gates.
        :return: List of gates ordered from the lower level to the higher level.
        """
        gates = []
        for node in LevelOrderIter(self.top_event):
            if type(node) is Gate:
                gates.append(node)
        return gates[::-1]

    def _get_basic_events(self):
        """
        Get basic events from Fault Tree Structure
        :return: Basic events
        """
        basic_events = []
        for node in self.top_event.descendants:
            if node.is_leaf:
                basic_events.append(node)
        return basic_events

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
        print(RenderTree(self.top_event))

    def export_time_series(self, file_name):
        """
        Export time series into a file called file_name.
        :param file_name: Name of the file with extension
        :return:
        """
        file = open(file_name, 'w')
        root = self.top_event
        for times in root.time_series:
            file.write('%s ' % times)
        file.write('\n')
        for basic_event in self._get_basic_events():
            for times in basic_event.time_series:
                file.write('%s ' % times)
            file.write('\n')

        file.close()

    def load_time_series_into_basic_events(self, time_series):
        basic_events = self._get_basic_events()
        for basic_event in basic_events:
            # basic_event.name[12:] is to only show numbers, ex: (Basic Event 12) => 12
            basic_event_id = int(basic_event.name[12:])
            # print(basic_event_id)
            # print(time_series[basic_event_id])
            basic_event.time_series = time_series[basic_event_id]

    def determine_distributions_of_basic_events(self):
        # NAME FOR THIS FUNCTION NOT ACCURATE, ACTUALLY CALCULATES MTTF AS OF NOW!!!
        time_series = TimeSeries('time_series.txt')
        basic_events = self._get_basic_events()
        for basic_event in basic_events:
            basic_event_id = int(basic_event.name[12:])
            basic_event.reliability_distribution = time_series.calculate_mean_time_to_failure(basic_event_id)

