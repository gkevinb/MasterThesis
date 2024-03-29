'''
import collections
import itertools
import importlib
from scipy.stats import expon, norm, weibull_min, lognorm
from scipy import integrate
import math, random
from functools import reduce
from anytree import NodeMixin, RenderTree, LevelOrderIter
from modules import logicgate, timeseries, distributionfitting as DF
from modules import cutsets, faultTreeReconstruction as ftr
from modules import distributionplotting as DP
import proxel
import numpy as np


DISPLAY_UP_TO = 6
# 'distributions', 'states', 'time_series'
EVENT_PRINT = 'distributions'

is_EVEN = lambda i: i % 2 == 0
is_ODD = lambda i: i % 2 == 1


class Event(NodeMixin):
    def __init__(self, name, reliability_distribution=None, maintainability_distribution=None, parent=None):
        self.name = name
        self.reliability_distribution = reliability_distribution
        self.maintainability_distribution = maintainability_distribution
        self.reliability_function = None
        self.maintainability_function = None
        self.MTTF = 0
        self.MTTR = 0
        self.availability_inherent = 0
        self.availability_operational = 0
        self.parent = parent
        self.time_series = []
        self.state = None
        self.proxel_time_series = []
        self.proxel_probability_of_failure = []

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

    def calculate_MTTF_from_time_series(self):
        self.MTTF = timeseries.calculate_mean_time_to_failure(self.time_series)

    def calculate_MTTR_from_time_series(self):
        self.MTTR = timeseries.calculate_mean_time_to_repair(self.time_series)

    def calculate_MTTF_from_distribution(self):
        self.MTTF = DF.calculate_mttf_or_mttr_from_distribution(self.reliability_distribution)

    def calculate_MTTR_from_distribution(self):
        self.MTTR = DF.calculate_mttf_or_mttr_from_distribution(self.maintainability_distribution)

    def calculate_inherent_availability(self):
        self.availability_inherent = self.MTTF/(self.MTTF + self.MTTR)

    def calculate_operational_availability(self, operating_cycle):
        self.availability_operational = timeseries.calculate_operational_availability(self.time_series, operating_cycle)

    def determine_reliability_distribution(self):
        time_of_failures = timeseries.calculate_time_to_failures(self.time_series)
        self.reliability_distribution = DF.determine_distribution(time_of_failures)

    def calculate_reliability_function(self, linspace):
        rel_dist = self.reliability_distribution
        if rel_dist[0] == 'EXP':
            lambda_ = rel_dist[1]
            scale_ = 1 / lambda_
            self.reliability_function = 1 - expon.cdf(linspace, scale=scale_)
        if rel_dist[0] == 'WEIBULL':
            scale = rel_dist[1]
            shape = rel_dist[2]
            self.reliability_function = 1 - weibull_min.cdf(linspace, shape, loc=0, scale=scale)
        if rel_dist[0] == 'NORMAL':
            mu = rel_dist[1]
            sigma = rel_dist[2]
            self.reliability_function = 1 - norm.cdf(linspace, loc=mu, scale=sigma)
        if rel_dist[0] == 'LOGNORM':
            mu = rel_dist[1]
            sigma = rel_dist[2]
            scale = math.exp(mu)
            self.reliability_function = 1 - lognorm.cdf(linspace, sigma, loc=0, scale=scale)

    def determine_maintainability_distribution(self):
        time_of_repairs = timeseries.calculate_time_to_repairs(self.time_series)
        self.maintainability_distribution = DF.determine_distribution(time_of_repairs)

    def calculate_maintainability_function(self, linspace):
        main_dist = self.maintainability_distribution
        if main_dist[0] == 'EXP':
            lambda_ = main_dist[1]
            scale_ = 1 / lambda_
            self.maintainability_function = expon.cdf(linspace, scale=scale_)
        if main_dist[0] == 'WEIBULL':
            scale = main_dist[1]
            shape = main_dist[2]
            self.maintainability_function = weibull_min.cdf(linspace, shape, loc=0, scale=scale)
        if main_dist[0] == 'NORMAL':
            mu = main_dist[1]
            sigma = main_dist[2]
            self.maintainability_function = norm.cdf(linspace, loc=mu, scale=sigma)
        if main_dist[0] == 'LOGNORM':
            mu = main_dist[1]
            sigma = main_dist[2]
            scale = math.exp(mu)
            self.maintainability_function = lognorm.cdf(linspace, sigma, loc=0, scale=scale)

    def calculate_probability_of_failure_using_proxel_based_method(self, delta_time, simulation_time):
        pn = proxel.ProxelNetwork(delta_time, simulation_time, self.reliability_distribution,
                                  self.maintainability_distribution)
        pn.expand_network()
        self.proxel_time_series = np.asarray(pn.time_series)
        self.proxel_probability_of_failure = np.asarray(pn.probability_of_failure)

    def __repr__(self):
        if EVENT_PRINT == 'time_series':
            return self.name + ' : ' + str(self.time_series[:DISPLAY_UP_TO])
        if EVENT_PRINT == 'distributions':
            return self.name + ' : ' + str(self.reliability_distribution) + ' : '\
                   + str(self.maintainability_distribution)
        if EVENT_PRINT == 'states':
            return self.name + ' : ' + str(self.state)
        else:
            return self.name


class Gate(NodeMixin):
    def __init__(self, name, parent=None, k=None):
        """
        ID is only for visualization purposes so each gate has a unique identifier when using DOT language.
        :param name:
        :param parent:
        :param k:
        """
        self.name = name
        self.id = random.randint(0, 1000000)
        self.parent = parent
        self.k = k

    def get_number_of_children(self):
        return len(self.children)

    def determine_fault_logic(self):
        fault_logic = None
        if self.name == 'AND':
            fault_logic = 'OR'
        if self.name == 'OR':
            fault_logic = 'AND'
        if self.name == 'VOTING':
            fault_logic = self.k

        return fault_logic

    def evaluate_time_series(self):
        """
        Evaluate the gate inputs and modify the gate output. Based on the gate type and gate input time series,
        calculate time series for gate output.
        Note: Fault tree gate logic is opposite, since it checks for failures not successes.
        :return:
        """
        data_streams = []
        for child in self.children:
            data_streams.append(child.time_series)

        fault_logic = self.determine_fault_logic()

        self.parent.time_series = logicgate.evaluate_time_series(fault_logic, data_streams)

    def evaluate_states(self):
        states = []

        for child in self.children:
            states.append(child.state)

        fault_logic = self.determine_fault_logic()

        self.parent.state = logicgate.evaluate_boolean_logic(fault_logic, states)

    def evaluate_reliability_maintainability(self):

        def k_N_voting(k, N, input_reliabilities):
            """
            Pseudocode on page 38 of Fault tree analysis: A survey of the state-of-the-art
            in modeling, analysis and tools
            Using recursion to calculate reliability when the gate is k/N Voting

            :param k:
            :param N:
            :param input_reliabilities:
            :return:
            """
            if k == 0:
                return 1
            if k == N:
                return reduce(lambda x, y: x * y, input_reliabilities)

            result = input_reliabilities[0] * k_N_voting(k - 1, N - 1, input_reliabilities[1:]) + \
                     (1 - input_reliabilities[0]) * k_N_voting(k, N - 1, input_reliabilities[1:])
            return result

        reliabilities = 1
        maintainabilities = 1

        if self.name == 'AND':
            for child in self.children:
                reliabilities *= (1 - child.reliability_function)
                maintainabilities *= (1 - child.maintainability_function)

            self.parent.reliability_function = 1 - reliabilities
            self.parent.maintainability_function = 1 - maintainabilities

        if self.name == 'OR':
            for child in self.children:
                reliabilities *= child.reliability_function
                maintainabilities *= child.maintainability_function

            self.parent.reliability_function = reliabilities
            self.parent.maintainability_function = maintainabilities

        if self.name == 'VOTING':
            child_reliability_functions = []
            child_maintainability_functions = []
            N = len(self.children)
            for child in self.children:
                child_reliability_functions.append(child.reliability_function)

                child_maintainability_functions.append(child.maintainability_function)

            self.parent.reliability_function = k_N_voting(self.k, N, child_reliability_functions)
            self.parent.maintainability_function = k_N_voting(self.k, N, child_maintainability_functions)

    def evaluate_proxel_probabilities(self):
        probabilities = 1
        if self.name == 'AND':
            for child in self.children:
                self.parent.proxel_time_series = child.proxel_time_series
                probabilities *= child.proxel_probability_of_failure

            self.parent.proxel_probability_of_failure = probabilities

        if self.name == 'OR':
            for child in self.children:
                self.parent.proxel_time_series = child.proxel_time_series
                probabilities *= (1 - child.proxel_probability_of_failure)

            self.parent.proxel_probability_of_failure = 1 - probabilities

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
        self.cut_sets = []
        self.minimal_cut_sets = []

        if top_event is not None:
            self.number_of_basic_events = len(self._get_basic_events())
        else:
            self.number_of_basic_events = 0

    @staticmethod
    def _get_id_of_basic_event(basic_event):
        # basic_event.name[12:] is to only show numbers, ex: (Basic Event 12) => 12
        return int(basic_event.name[12:])

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
        Get basic events from Fault Tree Structure, sorted numerically by name.
        :return: Basic events
        """
        basic_events = []
        for node in self.top_event.descendants:
            if node.is_leaf:
                basic_events.append(node)
        basic_events = sorted(basic_events, key=lambda event: event.name)

        return basic_events

    def get_basic_event_(self, basic_event_id):
        for basic_event in self._get_basic_events():
            if basic_event_id == self._get_id_of_basic_event(basic_event):
                return basic_event

        # If can't find it return None.
        return None

    def plot_reliability_distribution_of_basic_event_(self, basic_event_id, theoretical_distribution=None):
        basic_event = self.get_basic_event_(basic_event_id)
        name = basic_event.name
        reliability = 'Reliability'
        rel_dist = basic_event.reliability_distribution
        times = timeseries.calculate_time_to_failures(basic_event.time_series)

        DP.plot_distributions(name, reliability, rel_dist, times, theoretical_distribution)
        # IF CAN'T FIND DISTRIBUTION

    def plot_maintainability_distribution_of_basic_event_(self, basic_event_id, theoretical_distribution=None):
        basic_event = self.get_basic_event_(basic_event_id)
        name = basic_event.name
        maintainability = 'Maintainability'
        main_dist = basic_event.maintainability_distribution
        times = timeseries.calculate_time_to_repairs(basic_event.time_series)

        DP.plot_distributions(name, maintainability, main_dist, times, theoretical_distribution)

    def plot_reliability_distribution_of_top_event(self, linspace, theoretical=None):
        times = timeseries.calculate_time_to_failures(self.top_event.time_series)
        rel_dist = DF.determine_distribution(times)
        print('SUGGESTED RELIABILITY DISTRIBUTION FOR TOP EVENT: ' + str(rel_dist))
        DP.plot_arbitrary_distribution('Top Event', 'Reliability', times, linspace, theoretical)
        # DP.plot_weibull('Top Event', 'Reliability', rel_dist, times, theoretical)

    def plot_maintainability_distribution_of_top_event(self, linspace, theoretical=None):
        times = timeseries.calculate_time_to_repairs(self.top_event.time_series)
        main_dist = DF.determine_distribution(times)
        print('SUGGESTED MAINTAINABILITY DISTRIBUTION FOR TOP EVENT: ' + str(main_dist))
        DP.plot_arbitrary_distribution('Top Event', 'Maintainability', times, linspace, theoretical)
        # DP.plot_weibull('Top Event', 'Reliability', rel_dist, times, theoretical)

    def plot_probability_of_failure_of_basic_event_(self, basic_event_id):
        basic_event = self.get_basic_event_(basic_event_id)
        DP.plot_probability_of_failure(basic_event.proxel_time_series, basic_event.proxel_probability_of_failure)

    def plot_probability_of_failure_of_top_event(self):
        DP.plot_probability_of_failure(self.top_event.proxel_time_series, self.top_event.proxel_probability_of_failure)

    def get_top_event_state(self):
        return self.top_event.state

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
            gate.evaluate_time_series()

    def calculate_states(self):
        """
        Calculate states of all events except basic events.
        :return:
        """
        gates = self._get_gates_reversed()
        for gate in gates:
            gate.evaluate_states()

    def calculate_reliability_maintainability(self, linspace):
        for basic_event in self._get_basic_events():
            basic_event.calculate_reliability_function(linspace)
            basic_event.calculate_maintainability_function(linspace)

        gates = self._get_gates_reversed()
        for gate in gates:
            gate.evaluate_reliability_maintainability()

    def calculate_proxel_probalities(self, delta_time, simulation_time):
        for basic_event in self._get_basic_events():
            basic_event.calculate_probability_of_failure_using_proxel_based_method(delta_time, simulation_time)

        gates = self._get_gates_reversed()
        for gate in gates:
            gate.evaluate_proxel_probabilities()

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
        top_event = self.top_event
        for times in top_event.time_series:
            file.write('%s ' % times)
        file.write('\n')
        for basic_event in self._get_basic_events():
            for times in basic_event.time_series:
                file.write('%s ' % times)
            file.write('\n')

        file.close()

    def import_time_series(self, file_name):
        """
        Reads time series from the file given as file_name
        Places the times series of the top event as the first element in
        the dictionary and then all the basic events follow. The function
        also sets the number of basic events found in the file.
        :param file_name: Name of file
        :return:
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
            basic_event_id = self._get_id_of_basic_event(basic_event)
            basic_event.time_series = self.time_series[basic_event_id]

    def load_states_into_basic_events(self, states):
        basic_events = self._get_basic_events()
        i = 0
        for basic_event in basic_events:
            basic_event.state = states[i]
            i += 1

    def generate_truth_table(self):
        return list(itertools.product([True, False], repeat=self.number_of_basic_events))

    def export_truth_table(self, file_name=None):

        def convert_boolean_to_binary(boolean):
            if boolean is True:
                return 1
            else:
                return 0

        truth_table = self.generate_truth_table()

        file = open(file_name, 'w')

        for basic_event_id in self.basic_events_indexing():
            file.write('%s ' % basic_event_id)
        file.write('TE')
        file.write('\n')

        for row in truth_table:
            binaries = list(map(convert_boolean_to_binary, row))
            for binary in binaries:
                file.write('%s ' % binary)
            self.load_states_into_basic_events(row)
            self.calculate_states()
            binary = convert_boolean_to_binary(self.get_top_event_state())
            file.write('%s ' % binary)
            file.write('\n')

        file.close()

    def determine_distributions_of_basic_events(self):
        basic_events = self._get_basic_events()
        for basic_event in basic_events:
            basic_event.determine_reliability_distribution()
            basic_event.determine_maintainability_distribution()

    def basic_events_indexing(self):
        """
        self.number_of_basic_events + 1, the 1 is needed because go until that number.
        :return: The indexing of the basic events, useful for for loops in other methods to make code cleaner.
        """
        return range(self.basic_event_start_index, self.number_of_basic_events + 1)

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

    def calculate_MTTF_of_top_event_from_time_series(self):
        self.top_event.calculate_MTTF_from_time_series()

    def calculate_MTTR_of_top_event_from_time_series(self):
        self.top_event.calculate_MTTR_from_time_series()

    def calculate_MTTF_of_basic_events_from_time_series(self):
        for basic_event in self._get_basic_events():
            basic_event.calculate_MTTF_from_time_series()

    def calculate_MTTR_of_basic_events_from_time_series(self):
        for basic_event in self._get_basic_events():
            basic_event.calculate_MTTR_from_time_series()

    def calculate_inherent_availability_of_basic_events(self):
        for basic_event in self._get_basic_events():
            basic_event.calculate_inherent_availability()

    def calculate_inherent_availability_of_top_event(self):
        self.top_event.calculate_inherent_availability()

    def calculate_operational_availability_of_top_event(self, operating_cycle):
        self.top_event.calculate_operational_availability(operating_cycle)

    def calculate_MTTF_of_top_event_from_reliability_function(self, linspace):
        y_int = integrate.cumtrapz(self.top_event.reliability_function, linspace, initial=0)
        self.top_event.MTTF = y_int[-1]

    def calculate_MTTR_of_top_event_from_maintainability_function(self, linspace):
        # Its 1 - maintainability, since it has to be in the shape of reliability,
        # meaning it will go down to zero
        y_int = integrate.cumtrapz(1 - self.top_event.maintainability_function, linspace, initial=0)
        self.top_event.MTTR = y_int[-1]

    def calculate_MTTF_of_basic_events_from_distributions(self):
        for basic_event in self._get_basic_events():
            basic_event.calculate_MTTF_from_distribution()

    def calculate_MTTR_of_basic_events_from_distributions(self):
        for basic_event in self._get_basic_events():
            basic_event.calculate_MTTR_from_distribution()

    def print_MTTF_MTTR_of_basic_events(self):
        for basic_event in self._get_basic_events():
            print(basic_event.name)
            print('MTTF: ' + str(basic_event.MTTF))
            print('MTTR: ' + str(basic_event.MTTR))

    def print_distributions_of_basic_events(self):
        for basic_event in self._get_basic_events():
            print(basic_event.name)
            print('Reliability: ' + str(basic_event.reliability_distribution))
            print('Maintainability: ' + str(basic_event.maintainability_distribution))

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
        fault_tree_creator = importlib.import_module(module_name)
        self.top_event = fault_tree_creator.build_fault_tree()

    def get_length_of_top_event_time_series(self):
        return len(self.time_series[self.top_event_index])

    def check_if_top_event_same(self):
        # Check if recalculated top event time series are the same as the top event times series in the exported file.
        return self.top_event.time_series == self.time_series[self.top_event_index]
'''