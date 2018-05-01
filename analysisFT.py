from faultTreeContinuous import Event, Gate, FaultTree
import matplotlib.pyplot as plt
import numpy as np
from modules import distributionplotting as DP


def compare_reliability_of_basic_event_(basic_event_id, reconstructedFT, originalFT):
    original_basic_event = originalFT.get_basic_event_(basic_event_id)
    reconstructed_basic_event = reconstructedFT.get_basic_event_(basic_event_id)
    reconstructed_distribution = reconstructed_basic_event.reliability_distribution

    theoretical_distribution = original_basic_event.reliability_distribution
    reconstructedFT.plot_reliability_distribution_of_basic_event_(basic_event_id, theoretical_distribution)

    print(DP.mse_exp(theoretical_distribution, reconstructed_distribution))


def compare_maintainability_of_basic_event_(basic_event_id, reconstructedFT, originalFT):
    original_basic_event = originalFT.get_basic_event_(basic_event_id)

    theoretical_distribution = original_basic_event.maintainability_distribution
    reconstructedFT.plot_maintainability_distribution_of_basic_event_(basic_event_id, theoretical_distribution)


rel_exp_dist = ['EXP', 1/5]
lognorm_dist = ['LOGNORM', 4, 2]
norm_dist = ['NORMAL', 500, 40]
main_exp_dist = ['EXP', 1/2]
rel_weibull_dist = ['WEIBULL', 10, 8]
main_weibull_dist = ['WEIBULL', 4, 10]


topEvent = Event('Top Event')
or1 = Gate('OR', parent=topEvent)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=or1)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=or1)
intermed = Event('Inter event ', parent=or1)
and1 = Gate('AND', parent=intermed)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, main_exp_dist, parent=and1)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist, parent=and1)

'''
topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
vote2 = Gate('VOTING', parent=intermediateEvent1, k=2)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=vote2)
basicEvent2 = Event('Basic Event 2', rel_weibull_dist, main_exp_dist, parent=vote2)
intermediateEvent3 = Event('Intermediate Event 3', parent=vote2)
and2 = Gate('AND', parent=intermediateEvent3)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, rel_weibull_dist, parent=and2)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist,  parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent5 = Event('Basic Event 5', norm_dist, main_exp_dist, parent=or1)
intermediateEvent4 = Event('Intermediate Event 4', parent=or1)
and3 = Gate('AND', parent=intermediateEvent4)
basicEvent6 = Event('Basic Event 6', rel_exp_dist, lognorm_dist, parent=and3)
basicEvent7 = Event('Basic Event 7', lognorm_dist, main_exp_dist,  parent=and3)
basicEvent8 = Event('Basic Event 8', rel_exp_dist, norm_dist,  parent=and3)

'''

fault_tree = FaultTree(topEvent)
# 5000 takes about 30 seconds depending on FT complexity of course
# 10000 generation size takes a good minute
# 30000 takes more than 30 minutes didn't wait to finish
fault_tree.generate_basic_event_time_series(4000)
fault_tree.calculate_time_series()
fault_tree.print_tree()
#fault_tree.export_time_series('time_series.txt')

#fault_tree.plot_reliability_distribution_of_basic_event_(1)


# --------------------------START RECONSTRUCTION -------------------------------

FT = FaultTree()

FT.import_time_series('time_series_determined_weibull.txt')
FT.display_event_time_series(8)


print('Cut sets')
FT.calculate_cut_sets()
print('Minimal cut sets')
FT.calculate_minimal_cut_sets()
ts = FT.time_series[FT.top_event_index]
print('Top Event last timestamp: ' + str(ts[-1]))
length_of_top_event_time_series = len(ts)
number_of_times_of_failure_top_event = length_of_top_event_time_series/2

for i in range(1, FT.number_of_basic_events + 1):
    ts = FT.time_series[i]
    print('Basic Event ' + str(i) + ' last timestamp: ' + str(ts[-1]))


FT.reconstruct_fault_tree('generatedFT_method.py')
# Remember to take off .py extensive when using it as a module to be imported
FT.load_in_fault_tree('generatedFT_method')


FT.load_time_series_into_basic_events()

FT.calculate_MTTF_of_basic_events()
FT.calculate_MTTR_of_basic_events()
FT.print_MTTF_MTTR_of_basic_events()

FT.determine_distributions_of_basic_events()

FT.print_distributions_of_basic_events()

FT.print_tree()


#FT.plot_reliability_distribution_of_basic_event_(2)
#FT.plot_maintainability_distribution_of_basic_event_(3)

#compare_reliability_of_basic_event_(1, FT, fault_tree)
#compare_reliability_of_basic_event_(2, FT, fault_tree)
#compare_maintainability_of_basic_event_(1, FT, fault_tree)
compare_maintainability_of_basic_event_(2, FT, fault_tree)

# int(number_of_times_of_failure_top_event)
# doesn't have to be the same as times of failures for top event
linspace = np.linspace(0, 30, 1000)
fault_tree.calculate_reliability(linspace)

FT.calculate_time_series()

top_event_reliability = fault_tree.top_event.reliability_function
#print('Reliability at time 7: ' + str(top_event_reliability))
FT.plot_distribution_of_top_event(linspace, top_event_reliability)

'''
fig, subplot = plt.subplots(1, 1)
subplot.plot(linspace, fault_tree.top_event.reliability_function)
'''
plt.show()
