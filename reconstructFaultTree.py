from analyzeData import TimeSeries
from modules import distributionfitting as dF

time_series = TimeSeries('time_series.txt')
time_series.display_event_time_series(8)
print('Number of basic event: ' + str(time_series.number_of_basic_events))
TOP_EVENT = time_series.top_event_index

# Not working since I can't just determine distribution from time series but the differences between the times.
print(dF.determine_distribution(time_series.time_series[3]))

print('Mean time to failure: ' + str(time_series.calculate_mean_time_to_failure(TOP_EVENT)))
print('Mean time to repair: ' + str(time_series.calculate_mean_time_to_repair(TOP_EVENT)))
print('Cut sets')
time_series.calculate_cut_sets()
print('Minimal cut sets')
time_series.calculate_minimal_cut_sets()


# print('TimeSeries: ')
# print(time_series.time_series[2])


# time_series.reconstruct_fault_tree('generatedFT.py')
