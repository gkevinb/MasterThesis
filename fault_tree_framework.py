from modules.faulttree import FaultTree
from modules.faultTreeReconstruction import get_object_name
import fault_trees
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
    return fault_trees.A()


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

    operating_cycle = fault_tree.top_event.time_series[-1] * 0.4
    fault_tree.calculate_operational_availability_of_top_event(operating_cycle)

    for basic_event in fault_tree.get_basic_events():
        basic_event.calculate_operational_availability(operating_cycle)


def run_theoretical_analysis(fault_tree, linspace):
    fault_tree.calculate_reliability_maintainability(linspace)

    fault_tree.calculate_MTTF_of_basic_events_from_distributions()
    fault_tree.calculate_MTTR_of_basic_events_from_distributions()


def create_plots(reconstructed_fault_tree, original_fault_tree, linspace):
    for i in range(1, reconstructed_fault_tree.number_of_basic_events + 1):
        compare_reliability_of_basic_event_(i, reconstructed_fault_tree, original_fault_tree)
        compare_maintainability_of_basic_event_(i, reconstructed_fault_tree, original_fault_tree)
    reconstructed_fault_tree.plot_reliability_distribution_of_top_event()#linspace, original_fault_tree.top_event.reliability_function)
    reconstructed_fault_tree.plot_maintainability_distribution_of_top_event()#linspace, original_fault_tree.top_event.maintainability_function)


def get_info_on_events(fault_tree):
    events = []

    event_dictionary = {
        'event_name': get_object_name(fault_tree.top_event.name),
        'mtbf': fault_tree.top_event.MTTF,
        'mtbr': fault_tree.top_event.MTTR,
        'reliability': fault_tree.top_event.reliability_distribution,
        'maintainability': fault_tree.top_event.maintainability_distribution,
        'oper_avail': fault_tree.top_event.availability_operational
    }

    events.append(event_dictionary)

    for basic_event in fault_tree.get_basic_events():
        event_dictionary = {
            'event_name': get_object_name(basic_event.name),
            'mtbf': basic_event.MTTF,
            'mtbr': basic_event.MTTR,
            'reliability': basic_event.reliability_distribution,
            'maintainability': basic_event.maintainability_distribution,
            'oper_avail': basic_event.availability_operational
        }
        events.append(event_dictionary)

    return events


def export_info_to_json(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)
