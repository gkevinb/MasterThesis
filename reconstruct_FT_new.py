from faultTreeContinuous import Event, FaultTree

FT = FaultTree()
FT.read_time_series_from_file('time_series.txt')
FT.display_event_time_series(8)
print('Number of basic event: ' + str(FT.number_of_basic_events))
TOP_EVENT = FT.top_event_index


print('Mean time to failure: ' + str(FT.calculate_mean_time_to_failure(TOP_EVENT)))
print('Mean time to repair: ' + str(FT.calculate_mean_time_to_repair(TOP_EVENT)))
print('Cut sets')
FT.calculate_cut_sets()
print('Minimal cut sets')
FT.calculate_minimal_cut_sets()


# print('TimeSeries: ')
# print(time_series.time_series[2])


FT.reconstruct_fault_tree('generatedFT_new.py')
