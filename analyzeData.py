import collections


is_EVEN = lambda i: i % 2 == 0
is_ODD = lambda i: i % 2 == 1


class TimeSeries:

    def __init__(self, file_name):
        self.file_name = file_name
        self.time_series = {}
        self.top_event_index = 0
        self.basic_event_start_index = 1
        self.number_of_basic_events = self.read_time_series_from_file()
        self.cut_sets = []

    '''
    Reads time series from the file given in the __init__ function.
    Places the times series of the top event as the first element in 
    the dictionary and then all the basic events follow. The function
    returns the number of basic events found in the file.
    '''
    def read_time_series_from_file(self):
        file = open(self.file_name, 'r')
        dict_time_series = {}
        index = 0

        lines = file.readlines()
        for line in lines:
            event_time_series = []
            for time in line.split():
                event_time_series.append(float(time))
            dict_time_series[index] = event_time_series
            index += 1

            self.time_series = collections.OrderedDict(sorted(dict_time_series.items()))

        file.close()
        return index - 1

    # Returns the index of the basic events in list, used for for loops
    def basic_events_indexing(self):
        return range(self.basic_event_start_index, len(self.time_series))

    def display_event_time_series(self):
        print('Top Event : ' + str(self.time_series[self.top_event_index]))
        for i in self.basic_events_indexing():
            print('Basic Event ' + str(i) + ' : ' + str(self.time_series[i]))

    def get_time_differences(self, event):
        event_time_series = self.time_series[event]
        time_difference = 0
        times = []
        for time in event_time_series:
            times.append(time - time_difference)
            time_difference = time
        return times

    def get_mean_time_to_failure(self, event):
        times = self.get_time_differences(event)
        time_to_failures = []
        for i in range(len(times)):
            if is_EVEN(i):
                time_to_failures.append(times[i])
        print(time_to_failures)
        mean_time_to_failure = sum(time_to_failures)/len(time_to_failures)
        return mean_time_to_failure

    def get_mean_time_to_repair(self, event):
        times = self.get_time_differences(event)
        time_to_repair = []
        for i in range(len(times)):
            if is_ODD(i):
                time_to_repair.append(times[i])
        print(time_to_repair)
        mean_time_to_failure = sum(time_to_repair)/len(time_to_repair)
        return mean_time_to_failure

    def get_index_of_number_before(self, event, number):
        event_time_series = self.time_series[event]
        # For Testing: #event_time_series = [2, 4, 6]
        index = -1
        # First checks if number is smaller then the first number in series
        if number < event_time_series[0]:
            #print('FIRST')
            index = -1
        # Second checks if number is greater then the last number in series
        elif number > event_time_series[-1]:
            #print('LAST')
            index = len(event_time_series) - 1
        # Then checks the rest of the numbers
        else:
            #print('MIDDLE')
            for i in range(len(event_time_series)):
                if number < event_time_series[i]:
                    index = i - 1
                    break
        return index

    def get_state_of_event(self, event, time):
        index = self.get_index_of_number_before(event, time)
        if is_ODD(index):
            return 'UP'
        else:
            return 'DOWN'

    def get_state_of_basic_events(self, time):
        status_of_events = []
        for i in self.basic_events_indexing():
            status_of_events.append(self.get_state_of_event(i, time))
        #print(status_of_events)
        return status_of_events

    def get_all_cut_sets(self):
        top_event = self.time_series[self.top_event_index]
        all_cut_sets = {}
        for i in range(len(top_event)):
            if is_EVEN(i):
                failure = top_event[i]
                all_cut_sets[failure] = self.get_state_of_basic_events(failure)
        all_cut_sets = collections.OrderedDict(sorted(all_cut_sets.items()))
        print(all_cut_sets)
        return all_cut_sets

    def calculate_unique_cut_sets(self):
        all_cut_sets = self.get_all_cut_sets()
        unique_cut_sets = []
        for time, cut_set in all_cut_sets.items():
            if cut_set not in unique_cut_sets:
                unique_cut_sets.append(cut_set)
        return unique_cut_sets

    def convert_cut_set(self, symbol_cut_set):
        cut_set = []
        for i in range(len(symbol_cut_set)):
            if symbol_cut_set[i] == 'DOWN':
                cut_set.append(i + 1)
        return cut_set

    def convert_cut_sets(self):
        symbol_cut_sets = self.calculate_unique_cut_sets()
        for symbol_cut_set in symbol_cut_sets:
            self.cut_sets.append(self.convert_cut_set(symbol_cut_set))
        print('Cut sets: ' + str(self.cut_sets))
        return self.cut_sets


time_series = TimeSeries('testdata2.txt')
# time_series = TimeSeries('testfile.txt')
time_series.display_event_time_series()
# print('Number of basic event: ' + str(time_series.number_of_basic_events))
EVENT = time_series.top_event_index
#print('Mean time to failure: ' + str(time_series.get_mean_time_to_failure(EVENT)))
#print('Mean time to repair: ' + str(time_series.get_mean_time_to_repair(EVENT)))

time_series.convert_cut_sets()