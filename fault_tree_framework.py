from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree
from modules.faultTreeReconstruction import get_object_name
import json


def compare_reliability_of_basic_event_(basic_event_id, reconstructedFT, originalFT):
    original_basic_event = originalFT.get_basic_event_(basic_event_id)

    theoretical_distribution = original_basic_event.reliability_distribution
    reconstructedFT.plot_reliability_distribution_of_basic_event_(basic_event_id, theoretical_distribution)


def compare_maintainability_of_basic_event_(basic_event_id, reconstructedFT, originalFT):
    original_basic_event = originalFT.get_basic_event_(basic_event_id)

    theoretical_distribution = original_basic_event.maintainability_distribution
    reconstructedFT.plot_maintainability_distribution_of_basic_event_(basic_event_id, theoretical_distribution)


def create_fault_tree():

    rel_exp_dist = ['EXP', 1 / 3]
    main_exp_dist = ['EXP', 1 / 2]
    lognorm_dist = ['LOGNORM', 2, 1]
    norm_dist = ['NORMAL', 5, 1]

    top_event = Event("Top Event")
    and1 = Gate("AND", parent=top_event)
    intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
    intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
    voting2 = Gate("VOTING", parent=intermediate_event_1, k=2)
    basic_event_3 = Event("Basic Event 3", norm_dist, main_exp_dist, parent=voting2)
    basic_event_4 = Event("Basic Event 4", rel_exp_dist, main_exp_dist, parent=voting2)
    basic_event_5 = Event("Basic Event 5", norm_dist, main_exp_dist, parent=voting2)
    or3 = Gate("OR", parent=intermediate_event_2)
    basic_event_1 = Event("Basic Event 1", rel_exp_dist, main_exp_dist, parent=or3)
    basic_event_2 = Event("Basic Event 2", rel_exp_dist, main_exp_dist, parent=or3)

    fault_tree = FaultTree(top_event)

    return fault_tree


def generate_export_time_series(fault_tree, size, file_name):
    fault_tree.generate_basic_event_time_series(size)
    fault_tree.calculate_time_series()
    fault_tree.export_time_series(file_name)


def reconstruct_fault_tree(file_name):
    fault_tree = FaultTree()
    fault_tree.import_time_series(file_name)

    return fault_tree


def run_reconstruction_analysis(fault_tree):
    fault_tree.calculate_cut_sets()
    fault_tree.calculate_minimal_cut_sets()

    fault_tree.reconstruct_fault_tree('generatedFT_method.py')
    # Remember to take off .py extensive when using it as a module to be imported
    fault_tree.load_in_fault_tree('generatedFT_method')

    fault_tree.load_time_series_into_basic_events()

    fault_tree.determine_distributions_of_basic_events()

    fault_tree.calculate_time_series()

    fault_tree.calculate_MTTF_of_top_event_from_time_series()
    fault_tree.calculate_MTTR_of_top_event_from_time_series()

    fault_tree.calculate_MTTF_of_basic_events_from_time_series()
    fault_tree.calculate_MTTR_of_basic_events_from_time_series()

    operating_cycle = fault_tree.top_event.time_series[-1]
    fault_tree.calculate_operational_availability_of_top_event(operating_cycle)

    for basic_event in fault_tree.get_basic_events():
        basic_event.calculate_operational_availability(operating_cycle)


def run_theoretical_analysis(fault_tree, linspace):
    fault_tree.calculate_reliability_maintainability(linspace)

    fault_tree.calculate_MTTF_of_basic_events_from_distributions()
    fault_tree.calculate_MTTR_of_basic_events_from_distributions()

    fault_tree.calculate_inherent_availability_of_basic_events()


def create_plots(reconstructed_fault_tree, original_fault_tree):
    for i in range(1, reconstructed_fault_tree.number_of_basic_events + 1):
        compare_reliability_of_basic_event_(i, reconstructed_fault_tree, original_fault_tree)
        compare_maintainability_of_basic_event_(i, reconstructed_fault_tree, original_fault_tree)
    reconstructed_fault_tree.plot_reliability_distribution_of_top_event()
    reconstructed_fault_tree.plot_maintainability_distribution_of_top_event()


def get_info_on_events(fault_tree):
    events = []

    event_dictionary = {
        'event_name': get_object_name(fault_tree.top_event.name),
        'mtbf': fault_tree.top_event.MTTF,
        'mtbr': fault_tree.top_event.MTTR,
        'reliability_dist': fault_tree.top_event.reliability_distribution,
        'maitainability': fault_tree.top_event.maintainability_distribution,
        'oper_avail': fault_tree.top_event.availability_operational
    }

    events.append(event_dictionary)

    for basic_event in fault_tree.get_basic_events():
        event_dictionary = {
            'event_name': get_object_name(basic_event.name),
            'mtbf': basic_event.MTTF,
            'mtbr': basic_event.MTTR,
            'reliability_dist': basic_event.reliability_distribution,
            'maitainability': basic_event.maintainability_distribution,
            'oper_avail': basic_event.availability_operational
        }
        events.append(event_dictionary)

    return events


def export_info_to_json(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)
