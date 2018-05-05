from faultTreeContinuous import Event, Gate


def build_fault_tree():
    top_event = Event("Top Event")
    and1 = Gate("AND", parent=top_event)
    basic_event_1 = Event("Basic Event 1", parent=and1)
    basic_event_2 = Event("Basic Event 2", parent=and1)

    return top_event
