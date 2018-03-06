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

    def display_event_time_series(self):
        print('Top Event : ' + str(self.time_series[self.top_event_index]))
        for i in range(self.basic_event_start_index, len(self.time_series)):
            print('Basic Event ' + str(i) + ' : ' + str(self.time_series[i]))

    def get_time_differences(self, event):
        event_time_series = self.time_series[event]
        time_difference = 0
        times = []
        for time in event_time_series:
            times.append(time - time_difference)
            time_difference = time
        #print(times)
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


time_series = TimeSeries('time_series.txt')
# time_series = TimeSeries('testfile.txt')
time_series.display_event_time_series()
# print('Number of basic event: ' + str(time_series.number_of_basic_events))
EVENT = 0
print(time_series.get_mean_time_to_failure(EVENT))
print(time_series.get_mean_time_to_repair(EVENT))
