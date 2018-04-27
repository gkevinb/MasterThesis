from faultTreeContinuous import Gate, Event, FaultTree


topEvent = Event('Top Event')
or1 = Gate('OR', parent=topEvent)
basicEvent1 = Event('Basic Event 1', parent=or1)
basicEvent2 = Event('Basic Event 2', parent=or1)
basicEvent1.state = True
basicEvent2.state = True

FT = FaultTree(topEvent)
or1.evaluate_states()
FT.print_tree()