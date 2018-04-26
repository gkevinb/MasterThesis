import collections
import importlib
from anytree import NodeMixin, RenderTree, LevelOrderIter
from modules import logicgate, timeseries, distributionfitting as DF
from modules import cutsets, faultTreeReconstruction as ftr
# from generatedFT_method import build_fault_tree


DISPLAY_UP_TO = 6

is_EVEN = lambda i: i % 2 == 0
is_ODD = lambda i: i % 2 == 1


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
        return self.name + ' : ' + str(self.time_series[:DISPLAY_UP_TO])
        # MAKE THIS BETTER LATER!!!!!!!!
        # return self.name + ' : ' + str(self.reliability_distribution)


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
    def __init__(self, top_event=None):
        self.top_event = top_event
        self.time_series = {}
        self.top_event_index = 0
        self.basic_event_start_index = 1
        self.number_of_basic_events = 0
        self.cut_sets = []
        self.minimal_cut_sets = []

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

    def import_time_series(self, file_name):
        """
        Reads time series from the file given in the __init__ function.
        Places the times series of the top event as the first element in
        the dictionary and then all the basic events follow. The function
        returns the number of basic events found in the file.
        """
        file = open(file_name, 'r')
        time_series_dictionary = {}
        index = 0

        lines = file.readlines()
        for line in lines:
            event_time_series = []
            for time in line.split():
                event_time_series.append(float(time))
            time_series_dictionary[index] = event_time_series
            index += 1

        self.time_series = collections.OrderedDict(sorted(time_series_dictionary.items()))

        file.close()
        self.number_of_basic_events = index - 1

    def load_time_series_into_basic_events(self):
        basic_events = self._get_basic_events()
        for basic_event in basic_events:
            # basic_event.name[12:] is to only show numbers, ex: (Basic Event 12) => 12
            basic_event_id = int(basic_event.name[12:])
            # print(basic_event_id)
            # print(time_series[basic_event_id])
            basic_event.time_series = self.time_series[basic_event_id]

    def determine_distributions_of_basic_events(self):
        # THIS METHOD IS NOT FINISHED!!!!!
        basic_events = self._get_basic_events()
        for basic_event in basic_events:
            basic_event.reliability_distribution = DF.determine_distribution()

    def determine_mttf_of_basic_events(self):
        # THIS METHOD IS NOT FINISHED!!!!!!
        basic_events = self._get_basic_events()
        for basic_event in basic_events:
            basic_event_id = int(basic_event.name[12:])
            #basic_event.reliability_distribution = self.calculate_mean_time_to_failure(basic_event_id)

    def basic_events_indexing(self):
        """
        :return: The indexing of the basic events, useful for for loops in other methods to make code cleaner.
        """
        return range(self.basic_event_start_index, len(self.time_series))

    def get_basic_events_time_series(self):
        """
        Get time series of basic events.
        :return: List of time series of the basic events.
        """
        basic_events = []
        for i in self.basic_events_indexing():
            basic_events.append(self.time_series[i])
        return basic_events

    def display_event_time_series(self, display_up_to=-1):
        """
        Display the time series for the top event and the basic events.
        :param display_up_to: Displays time series up to display_up_to, default is -1 to display all.
        :return:
        """
        print('Top Event : ' + str(self.time_series[self.top_event_index][:display_up_to]))
        for i in self.basic_events_indexing():
            print('Basic Event ' + str(i) + ' : ' + str(self.time_series[i][:display_up_to]))

    def calculate_time_differences(self, event):
        """
        Calculate time differences from the time series to get the times. Basically subtracts the previous time from
        the next time to get the difference between the time series times.
        :param event: The event of which we need the time series of.
        :return: The time differences extracted from the time series.
        """
        event_time_series = self.time_series[event]
        time_difference = 0
        times = []
        for time in event_time_series:
            times.append(time - time_difference)
            time_difference = time
        return times

    def calculate_mean_time_to_failure(self, event):
        """
        Calculate mean time to failure for a certain event
        :param event: The event to calculate the mean time to failure of.
        :return: Mean time to failure
        """
        times = self.calculate_time_differences(event)
        time_to_failures = []
        for i in range(len(times)):
            if is_EVEN(i):
                time_to_failures.append(times[i])

        mean_time_to_failure = sum(time_to_failures)/len(time_to_failures)
        return mean_time_to_failure

    def calculate_mean_time_to_repair(self, event):
        """
        Calculate mean time to repair for a certain event
        :param event: The event to calculate the mean time to repair of.
        :return: Mean time to repair
        """
        times = self.calculate_time_differences(event)
        time_to_repair = []
        for i in range(len(times)):
            if is_ODD(i):
                time_to_repair.append(times[i])

        mean_time_to_repair = sum(time_to_repair)/len(time_to_repair)
        return mean_time_to_repair

    def calculate_cut_sets(self):
        """
        Calculate the cut sets of the fault tree.
        :return:
        """
        top_event = self.time_series[self.top_event_index]
        basic_events = self.get_basic_events_time_series()
        self.cut_sets = cutsets.calculate_cut_sets(top_event, basic_events)
        print(self.cut_sets)

    def calculate_minimal_cut_sets(self):
        """
        Calculate the minimal cut sets from the cut sets.
        :return:
        """
        self.minimal_cut_sets = cutsets.calculate_minimal_cut_sets(self.cut_sets)
        print(self.minimal_cut_sets)

    def get_minimal_cut_sets(self):
        return self.minimal_cut_sets

    def reconstruct_fault_tree(self, file_name):
        ftr.reconstruct_fault_tree(self.minimal_cut_sets, file_name)

    def load_in_fault_tree(self, module_name):
        custom_module = importlib.import_module(module_name)
        self.top_event = custom_module.build_fault_tree()

    def get_length_of_top_event_time_series(self):
        return len(self.time_series[self.top_event_index])

    def check_if_top_event_same(self):
        # Check if recalculated top event time series are the same as the top event times series in the exported file.
        print(self.top_event.time_series)
        print(self.time_series[self.top_event_index])
        return self.top_event.time_series == self.time_series[self.top_event_index]
