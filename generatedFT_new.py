from faultTreeContinuous import Event, Gate, FaultTree


top_event = Event("Top Event")
and1 = Gate("AND", parent=top_event)
intermediate_event_1 = Event("Intermediate Event 1", parent=and1)
intermediate_event_2 = Event("Intermediate Event 2", parent=and1)
or2 = Gate("OR", parent=intermediate_event_1)
intermediate_event_3 = Event("Intermediate Event 3", parent=or2)
basic_event_5 = Event("Basic Event 5", parent=or2)
voting3 = Gate("VOTING", parent=intermediate_event_2, k=2)
intermediate_event_4 = Event("Intermediate Event 4", parent=voting3)
basic_event_1 = Event("Basic Event 1", parent=voting3)
basic_event_2 = Event("Basic Event 2", parent=voting3)
and4 = Gate("AND", parent=intermediate_event_3)
basic_event_6 = Event("Basic Event 6", parent=and4)
basic_event_7 = Event("Basic Event 7", parent=and4)
basic_event_8 = Event("Basic Event 8", parent=and4)
and5 = Gate("AND", parent=intermediate_event_4)
basic_event_3 = Event("Basic Event 3", parent=and5)
basic_event_4 = Event("Basic Event 4", parent=and5)

fault_tree = FaultTree(top_event)
fault_tree.print_tree()
