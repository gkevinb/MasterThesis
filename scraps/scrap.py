import itertools
from faultTreeContinuous import Gate, Event, FaultTree


topEvent = Event('Top Event')
or1 = Gate('OR', parent=topEvent)
basicEvent1 = Event('Basic Event 1', parent=or1)
basicEvent2 = Event('Basic Event 2', parent=or1)

FT = FaultTree(topEvent)

FT.print_tree()
# print('Top Event status: ' + str(FT.top_event.state))
n = 2
# Can switch True False around
table = list(itertools.product([True, False], repeat=n))
for row in table:
    # print('Row: ' + str(row))
    FT.load_states_into_basic_events(row)
    FT.calculate_states()
    # print('Result: ' + str(FT.top_event.state))
    FT.print_tree()
