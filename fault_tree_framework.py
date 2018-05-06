from modules.gate import Gate
from modules.event import Event
from modules.faulttree import FaultTree


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

    top_event = Event("Top Event")
    and1 = Gate("AND", parent=top_event)
    intermediate_event_1 = Event("Intermediate Event 1", rel_exp_dist, main_exp_dist, parent=and1)
    intermediate_event_2 = Event("Intermediate Event 2", rel_exp_dist, main_exp_dist, parent=and1)
    voting2 = Gate("VOTING", parent=intermediate_event_1, k=2)
    basic_event_3 = Event("Basic Event 3", rel_exp_dist, main_exp_dist, parent=voting2)
    basic_event_4 = Event("Basic Event 4", rel_exp_dist, main_exp_dist, parent=voting2)
    basic_event_5 = Event("Basic Event 5", rel_exp_dist, main_exp_dist, parent=voting2)
    and3 = Gate("AND", parent=intermediate_event_2)
    basic_event_1 = Event("Basic Event 1", rel_exp_dist, main_exp_dist, parent=and3)
    basic_event_2 = Event("Basic Event 2", rel_exp_dist, main_exp_dist, parent=and3)

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


def run_reconstruction_analysis(fault_tree, operating_cycle):
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

    fault_tree.calculate_operational_availability_of_top_event(operating_cycle)


def run_theoretical_analysis(fault_tree, linspace, operating_cycle):
    fault_tree.calculate_reliability_maintainability(linspace)

    fault_tree.calculate_MTTF_of_basic_events_from_distributions()
    fault_tree.calculate_MTTR_of_basic_events_from_distributions()

    fault_tree.calculate_inherent_availability_of_basic_events()

    fault_tree.calculate_operational_availability_of_top_event(operating_cycle)


def create_plots(reconstructed_fault_tree, original_fault_tree):
    for i in range(1, reconstructed_fault_tree.number_of_basic_events + 1):
        compare_reliability_of_basic_event_(i, reconstructed_fault_tree, original_fault_tree)
