import collections
import cutsets


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
        self.minimal_cut_sets = []

    def read_time_series_from_file(self):
        """
        Reads time series from the file given in the __init__ function.
        Places the times series of the top event as the first element in
        the dictionary and then all the basic events follow. The function
        returns the number of basic events found in the file.
        """
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

    def get_basic_events(self):
        basic_events = []
        for i in self.basic_events_indexing():
            basic_events.append(self.time_series[i])
        return basic_events

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
        #print(time_to_failures)
        mean_time_to_failure = sum(time_to_failures)/len(time_to_failures)
        return mean_time_to_failure

    def get_mean_time_to_repair(self, event):
        times = self.get_time_differences(event)
        time_to_repair = []
        for i in range(len(times)):
            if is_ODD(i):
                time_to_repair.append(times[i])
        #print(time_to_repair)
        mean_time_to_failure = sum(time_to_repair)/len(time_to_repair)
        return mean_time_to_failure

    def calculate_cut_sets(self):
        top_event = self.time_series[self.top_event_index]
        basic_events = self.get_basic_events()
        self.cut_sets = cutsets.convert_cut_sets(top_event, basic_events)
        print(self.cut_sets)

    def calculate_minimal_cut_sets(self):
        self.minimal_cut_sets = cutsets.calculate_minimal_cut_sets(self.cut_sets)
        print(self.minimal_cut_sets)


time_series = TimeSeries('testdata2.txt')
# time_series = TimeSeries('testfile.txt')
time_series.display_event_time_series()
print('Number of basic event: ' + str(time_series.number_of_basic_events))
TOP_EVENT = time_series.top_event_index
print('Mean time to failure: ' + str(time_series.get_mean_time_to_failure(TOP_EVENT)))
print('Mean time to repair: ' + str(time_series.get_mean_time_to_repair(TOP_EVENT)))
print('Cut sets')
time_series.calculate_cut_sets()
print('Minimal cut sets')
time_series.calculate_minimal_cut_sets()
