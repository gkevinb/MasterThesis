from faultTreeContinuous import Event, Gate


def build_fault_tree():
    top_event = Event("Top Event")
    or1 = Gate("OR", parent=top_event)
    intermediate_event_1 = Event("Intermediate Event 1", parent=or1)
    basic_event_1 = Event("Basic Event 1", parent=or1)
    basic_event_2 = Event("Basic Event 2", parent=or1)
    and2 = Gate("AND", parent=intermediate_event_1)
    basic_event_3 = Event("Basic Event 3", parent=and2)
    basic_event_4 = Event("Basic Event 4", parent=and2)

    return top_event
