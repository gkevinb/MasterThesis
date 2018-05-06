from modules.gate import Gate
from modules.event import Event


def build_fault_tree():
    top_event = Event("Top Event")
    and1 = Gate("AND", parent=top_event)
    intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
    intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
    voting2 = Gate("VOTING", parent=intermediate_event_1, k=2)
    basic_event_3 = Event("Basic Event 3", parent=voting2)
    basic_event_4 = Event("Basic Event 4", parent=voting2)
    basic_event_5 = Event("Basic Event 5", parent=voting2)
    and3 = Gate("AND", parent=intermediate_event_2)
    basic_event_1 = Event("Basic Event 1", parent=and3)
    basic_event_2 = Event("Basic Event 2", parent=and3)

    return top_event
