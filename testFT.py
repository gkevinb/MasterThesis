from faultTreeContinuous import Event, Gate, FaultTree


top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
and2 = Gate("AND", parent=intermediate_event_1)
basic_event_1 = Event("Basic Event 1", parent=and2)
basic_event_2 = Event("Basic Event 2", parent=and2)
or3 = Gate("OR", parent=intermediate_event_2)
basic_event_3 = Event("Basic Event 3", parent=or3)
basic_event_4 = Event("Basic Event 4", parent=or3)

fault_tree = FaultTree(top_event)
fault_tree.print_tree()
