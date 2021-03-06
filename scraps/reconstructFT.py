from faultTreeContinuous import FaultTree
import time
import numpy as np
import matplotlib.pyplot as plt


start = time.time()


FT = FaultTree()

FT.import_time_series('time_series.txt')
FT.display_event_time_series(8)
print('Number of basic event: ' + str(FT.number_of_basic_events))
TOP_EVENT = FT.top_event_index

print('Length of top event: ' + str(FT.get_length_of_top_event_time_series()))
#print('Mean time to failure: ' + str(FT.calculate_mean_time_to_failure(TOP_EVENT)))
#print('Mean time to repair: ' + str(FT.calculate_mean_time_to_repair(TOP_EVENT)))

print('Cut sets')
FT.calculate_cut_sets()
print('Minimal cut sets')
FT.calculate_minimal_cut_sets()


# minimal_cut_sets = ((1, 2), (1, 3), (2, 3))
# minimal_cut_sets = [[1, 3, 4, 5], [1, 3, 4, 6, 7], [2, 3, 4, 6, 7], [1, 2, 6, 7], [1, 2, 5], [2, 3, 4, 5]]
# print('TimeSeries: ')
# print(time_series.time_series[2])

# FT.minimal_cut_sets = minimal_cut_sets


# Checks the last timestamp for each basic event time series, to see if enough
# data has been generated to do analysis on.
ts = FT.time_series[TOP_EVENT]
print('Top Event last timestamp: ' + str(ts[-1]))

for i in range(1, FT.number_of_basic_events + 1):
    ts = FT.time_series[i]
    print('Basic Event ' + str(i) + ' last timestamp: ' + str(ts[-1]))


FT.reconstruct_fault_tree('generatedFT_method.py')
# Remember to take off .py extensive when using it as a module to be imported
FT.load_in_fault_tree('generatedFT_method')


FT.load_time_series_into_basic_events()
FT.calculate_MTTF_of_basic_events_from_time_series()
FT.calculate_MTTR_of_basic_events_from_time_series()

FT.print_MTTF_MTTR_of_basic_events()

FT.determine_distributions_of_basic_events()

FT.print_distributions_of_basic_events()

FT.print_tree()

rel_exp_dist = ['EXP', 1/40]
lognorm = ['LOGNORM', 2, 1]
norm = ['NORMAL', 15, 2]
main_exp_dist = ['EXP', 1/10]
rel_weibull_dist = ['WEIBULL', 10, 8]
main_weibull_dist = ['WEIBULL', 4, 10]

FT.plot_reliability_distribution_of_basic_event_(2, rel_weibull_dist)
FT.plot_maintainability_distribution_of_basic_event_(3, lognorm)

plt.show()
'''
FT.calculate_time_series()

FT.print_tree()

print('Top events same: ')
print(FT.check_if_top_event_same())

FT.export_truth_table('truth_table_reconstructed.txt')

# FT.plot_maintainability_distribution_of_basic_event_(6)


linspace = np.linspace(0, 100, 1000)
FT.calculate_reliability(linspace)

# print(FT.top_event.reliability_function)

fig, subplot = plt.subplots(1, 1)
subplot.plot(linspace, FT.top_event.reliability_function)
subplot.set_title('Top event calculated')
plt.show(block=False)

FT.plot_distribution_of_top_event()

print('It took', time.time() - start, 'seconds.')
'''