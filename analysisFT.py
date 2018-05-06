from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree
import matplotlib.pyplot as plt
import numpy as np
from modules import distributionplotting as DP


def compare_reliability_of_basic_event_(basic_event_id, reconstructedFT, originalFT):
    original_basic_event = originalFT.get_basic_event_(basic_event_id)
    #reconstructed_basic_event = reconstructedFT.get_basic_event_(basic_event_id)
    #reconstructed_distribution = reconstructed_basic_event.reliability_distribution

    theoretical_distribution = original_basic_event.reliability_distribution
    reconstructedFT.plot_reliability_distribution_of_basic_event_(basic_event_id, theoretical_distribution)

    #print(DP.mse_exp(theoretical_distribution, reconstructed_distribution))


def compare_maintainability_of_basic_event_(basic_event_id, reconstructedFT, originalFT):
    original_basic_event = originalFT.get_basic_event_(basic_event_id)

    theoretical_distribution = original_basic_event.maintainability_distribution
    reconstructedFT.plot_maintainability_distribution_of_basic_event_(basic_event_id, theoretical_distribution)


def compare_reliability_of_top_event(linspace, reconstructedFT, originalFt):
    top_event_reliability = originalFt.top_event.reliability_function

    reconstructedFT.plot_reliability_distribution_of_top_event(linspace, top_event_reliability)


def compare_maintainability_of_top_event(linspace, reconstructedFT, originalFt):
    top_event_maintainability = originalFt.top_event.maintainability_function

    reconstructedFT.plot_maintainability_distribution_of_top_event(linspace, top_event_maintainability)


def compare_MTTF_MTTR_of_top_event(reconstructedFT, originalFT):
    print('Reconstructed Fault Tree: ')
    print('MTTF from time series: ' + str(reconstructedFT.top_event.MTTF))
    print('MTTR from time series: ' + str(reconstructedFT.top_event.MTTR))

    print('Original Fault Tree: ')
    print('MTTF from reliability function: ' + str(originalFT.top_event.MTTF))
    print('MTTR from maintainability function: ' + str(originalFT.top_event.MTTR))
    print('----------------------------------------------------------------')


def compare_MTTF_MTTR_of_basic_events(reconstructedFT, originalFT):
    basic_event_names = []
    reconstructedMTTF = []
    reconstructedMTTR = []
    originalMTTF = []
    originalMTTR = []
    for basic_event in reconstructedFT._get_basic_events():
        basic_event_names.append(basic_event.name)
        reconstructedMTTF.append(basic_event.MTTF)
        reconstructedMTTR.append(basic_event.MTTR)

    for basic_event in originalFT._get_basic_events():
        originalMTTF.append(basic_event.MTTF)
        originalMTTR.append(basic_event.MTTR)

    print('Reconstructed\t\t\t\tOriginal')
    for i in range(0, len(basic_event_names)):
        print(basic_event_names[i])
        print('MTTF: ' + str(reconstructedMTTF[i]) + '\t\t\t' + str(originalMTTF[i]))
        print('MTTR: ' + str(reconstructedMTTR[i]) + '\t\t\t' + str(originalMTTR[i]))
    print('----------------------------------------------------------------')


def compare_distributions_of_basic_events(reconstructedFT, originalFT):
    basic_event_names = []
    reconstructed_reliability = []
    reconstructed_maintainability = []
    original_reliability = []
    original_maintainability = []
    for basic_event in reconstructedFT._get_basic_events():
        basic_event_names.append(basic_event.name)
        reconstructed_reliability.append(basic_event.reliability_distribution)
        reconstructed_maintainability.append(basic_event.maintainability_distribution)

    for basic_event in originalFT._get_basic_events():
        original_reliability.append(basic_event.reliability_distribution)
        original_maintainability.append(basic_event.maintainability_distribution)

    print('Reconstructed\t\t\t\tOriginal')
    for i in range(0, len(basic_event_names)):
        print(basic_event_names[i])
        print('Reliability: ' + str(reconstructed_reliability[i]) + '\t\t\t' + str(original_reliability[i]))
        print('Maintainability: ' + str(reconstructed_maintainability[i]) + '\t\t\t' + str(original_maintainability[i]))
    print('----------------------------------------------------------------')


def compare_inherent_availability_of_basic_events(reconstructedFT, originalFT):
    basic_event_names = []
    reconstructed_availability_inherent = []
    original_availability_inherent = []
    for basic_event in reconstructedFT._get_basic_events():
        basic_event_names.append(basic_event.name)
        reconstructed_availability_inherent.append(basic_event.availability_inherent)

    for basic_event in originalFT._get_basic_events():
        original_availability_inherent.append(basic_event.availability_inherent)

    print('Reconstructed Fault Tree\t\t\t\t\t\tOriginal Fault Tree')
    for i in range(0, len(basic_event_names)):
        print(basic_event_names[i])
        print('Inherent Availability: ' + str(reconstructed_availability_inherent[i]) +
              '\t\t\t' + str(original_availability_inherent[i]))
    print('----------------------------------------------------------------')


def compare_availabilities_of_top_event(reconstructedFT, originalFT):
    print('Reconstructed Fault Tree\t\t\t\t\t\tOriginal Fault Tree')
    print('Top Event')
    print('Inherent Availability: ' + str(reconstructedFT.top_event.availability_inherent) +
          '\t\t\t' + str(originalFT.top_event.availability_inherent))
    print('Operational Availability: ' + str(reconstructedFT.top_event.availability_operational) +
          '\t\t\t' + str(originalFT.top_event.availability_operational))


def run_reconstruction_analysis(faultTree):
    print('Cut sets')
    faultTree.calculate_cut_sets()
    print('Minimal cut sets')
    faultTree.calculate_minimal_cut_sets()

    faultTree.reconstruct_fault_tree('generatedFT_method.py')
    # Remember to take off .py extensive when using it as a module to be imported
    faultTree.load_in_fault_tree('generatedFT_method')

    faultTree.load_time_series_into_basic_events()

    faultTree.determine_distributions_of_basic_events()

    faultTree.calculate_time_series()

    faultTree.calculate_MTTF_of_top_event_from_time_series()
    faultTree.calculate_MTTR_of_top_event_from_time_series()

    faultTree.calculate_MTTF_of_basic_events_from_time_series()
    faultTree.calculate_MTTR_of_basic_events_from_time_series()

    faultTree.calculate_inherent_availability_of_basic_events()
    faultTree.calculate_inherent_availability_of_top_event()

    faultTree.calculate_operational_availability_of_top_event(30000)


def run_theoretical_analysis(faultTree, linspace):
    faultTree.calculate_reliability_maintainability(linspace)

    faultTree.calculate_MTTF_of_top_event_from_reliability_function(linspace)
    faultTree.calculate_MTTR_of_top_event_from_maintainability_function(linspace)

    faultTree.calculate_MTTF_of_basic_events_from_distributions()
    faultTree.calculate_MTTR_of_basic_events_from_distributions()

    faultTree.calculate_inherent_availability_of_basic_events()
    faultTree.calculate_inherent_availability_of_top_event()

    faultTree.calculate_operational_availability_of_top_event(30000)


# --------------------PROGRAM STARTS HERE-------------------------

rel_weibull_dist = ['WEIBULL', 60, 10]
main_weibull_dist = ['WEIBULL', 4, 10]

rel_exp_dist = ['EXP', 1 / 10]
lognorm_dist = ['LOGNORM', 2, 1]
norm_dist = ['NORMAL', 12, 1]
main_exp_dist = ['EXP', 1 / 2]
'''
topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=and1)
basicEvent2 = Event('Basic Event 2', ['EXP', 1 / 100], main_exp_dist, parent=and1)

'''
'''
intermed = Event('Inter event ', parent=or1)
and1 = Gate('AND', parent=intermed)
basicEvent3 = Event('Basic Event 3', lognorm_dist, norm_dist, parent=and1)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist, parent=and1)
'''

topEvent = Event('Top Event')
and1 = Gate('AND', parent=topEvent)
intermediateEvent1 = Event('Intermediate Event 1', parent=and1)
intermediateEvent2 = Event('Intermediate Event 2', parent=and1)
vote2 = Gate('VOTING', parent=intermediateEvent1, k=2)
basicEvent1 = Event('Basic Event 1', rel_exp_dist, main_exp_dist, parent=vote2)
basicEvent2 = Event('Basic Event 2', rel_exp_dist, main_exp_dist, parent=vote2)
intermediateEvent3 = Event('Intermediate Event 3', parent=vote2)
and2 = Gate('AND', parent=intermediateEvent3)
basicEvent3 = Event('Basic Event 3', rel_exp_dist, main_exp_dist, parent=and2)
basicEvent4 = Event('Basic Event 4', rel_exp_dist, main_exp_dist,  parent=and2)
or1 = Gate('OR', parent=intermediateEvent2)
basicEvent5 = Event('Basic Event 5', rel_exp_dist, main_exp_dist, parent=or1)
intermediateEvent4 = Event('Intermediate Event 4', parent=or1)
and3 = Gate('AND', parent=intermediateEvent4)
basicEvent6 = Event('Basic Event 6', rel_exp_dist, main_exp_dist, parent=and3)
basicEvent7 = Event('Basic Event 7', rel_exp_dist, main_exp_dist,  parent=and3)
basicEvent8 = Event('Basic Event 8', rel_exp_dist, main_exp_dist,  parent=and3)



fault_tree = FaultTree(topEvent)
# 5000 takes about 30 seconds depending on FT complexity of course
# 10000 generation size takes a good minute
# 30000 takes more than 30 minutes didn't wait to finish
fault_tree.generate_basic_event_time_series(4000)
fault_tree.calculate_time_series()
fault_tree.print_tree()
fault_tree.export_time_series('time_series.txt')


# --------------------------START RECONSTRUCTION -------------------------------

FT = FaultTree()
FT.import_time_series('time_series.txt')
FT.display_event_time_series(8)


run_reconstruction_analysis(FT)

linspace = np.linspace(0, 1500, 15000)

run_theoretical_analysis(fault_tree, linspace)

ts = FT.time_series[FT.top_event_index]
print('Top Event last timestamp: ' + str(ts[-1]))
length_of_top_event_time_series = len(ts)
number_of_times_of_failure_top_event = length_of_top_event_time_series/2

for i in range(1, FT.number_of_basic_events + 1):
    ts = FT.time_series[i]
    print('Basic Event ' + str(i) + ' last timestamp: ' + str(ts[-1]))

FT.print_tree()

# int(number_of_times_of_failure_top_event)
# doesn't have to be the same as times of failures for top event

compare_reliability_of_basic_event_(1, FT, fault_tree)
#compare_reliability_of_top_event(linspace, FT, fault_tree)
#compare_maintainability_of_top_event(linspace, FT, fault_tree)
FT.plot_maintainability_distribution_of_top_event()
FT.plot_reliability_distribution_of_top_event()

print('------------------------------------------------------------')

compare_MTTF_MTTR_of_top_event(FT, fault_tree)
compare_MTTF_MTTR_of_basic_events(FT, fault_tree)
compare_distributions_of_basic_events(FT, fault_tree)
compare_inherent_availability_of_basic_events(FT, fault_tree)
compare_availabilities_of_top_event(FT, fault_tree)

FT.export_to_png('Reconstruced_FT.png')
fault_tree.export_to_png('Original_FT.png')

'''
fig, subplot = plt.subplots(1, 1)
subplot.plot(linspace, fault_tree.top_event.reliability_function)
'''
plt.show()
