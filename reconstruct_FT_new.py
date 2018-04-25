from faultTreeContinuous import FaultTree

FT = FaultTree()
FT.import_time_series('time_series_2.txt')
FT.display_event_time_series(8)
print('Number of basic event: ' + str(FT.number_of_basic_events))
TOP_EVENT = FT.top_event_index

print('Length of top event: ' + str(FT.get_length_of_top_event_time_series()))
print('Mean time to failure: ' + str(FT.calculate_mean_time_to_failure(TOP_EVENT)))
print('Mean time to repair: ' + str(FT.calculate_mean_time_to_repair(TOP_EVENT)))
print('Cut sets')
FT.calculate_cut_sets()
print('Minimal cut sets')
FT.calculate_minimal_cut_sets()

# minimal_cut_sets = ((1, 2), (1, 3), (2, 3))
# minimal_cut_sets = [[1, 3, 4, 5], [1, 3, 4, 6, 7], [2, 3, 4, 6, 7], [1, 2, 6, 7], [1, 2, 5], [2, 3, 4, 5]]
# print('TimeSeries: ')
# print(time_series.time_series[2])

# FT.minimal_cut_sets = minimal_cut_sets


ts = FT.time_series[TOP_EVENT]
print('Top Event last timestamp: ' + str(ts[-1]))

for i in range(1, FT.number_of_basic_events + 1):
    ts = FT.time_series[i]
    print('Basic Event ' + str(i) + ' last timestamp: ' + str(ts[-1]))

FT.reconstruct_fault_tree('generatedFT_new.py')
