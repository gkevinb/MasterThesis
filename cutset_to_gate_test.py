import cutset_to_gate as c2g


# cut_sets = [[1, 2], [3, 4]]
cut_sets = [[1, 3], [1, 4], [2, 3], [2, 4]]
# cut_sets = ((1,), (2,))
# cut_sets = ((1, 2), (3,), (4,))
# CANT HANDLE # cut_sets = (1, 2) BECAUSE IT IS ONLY ONE CUT SET,
# SO WRITE THIS INSTEAD:
# cut_sets = ((1, 2),)

print('Cut Sets:')

for cut_set in cut_sets:
    print(cut_set)

print('Basic Events:')
basic_events = c2g.get_basic_events(cut_sets)
print(basic_events)


set1 = {1, 2}
set2 = {1, 2}


print('Identical: ' + str(c2g.is_sets_identical(set1, set2)))

print('Mutually Exclusive: ' + str(c2g.is_sets_mutually_exclusive(set1, set2)))

'''
c2g.print_event_dictionary(event_dict)

identical_sets = c2g.find_identical_sets(event_dict)
print('Identical sets: ' + str(identical_sets))

c2g.print_event_dictionary(identical_sets)

mutual_exclusive_sets = c2g.find_mutual_exclusive_sets(identical_sets)
print('Mutual Exclusive sets: ' + str(mutual_exclusive_sets))

c2g.print_event_dictionary(mutual_exclusive_sets)
'''

entire_event_dict = {}
event_dict = c2g.create_event_cut_set_dict(basic_events, cut_sets)

entire_event_dict.update(event_dict)

print('--------------------------------------')
c2g.print_event_dictionary(event_dict)
while len(event_dict) != 1:
    event_dict = c2g.find_identical_sets(event_dict)
    print('--------------------------------------')
    c2g.print_event_dictionary(event_dict)
    entire_event_dict.update(event_dict)

    event_dict = c2g.find_mutual_exclusive_sets(event_dict)
    print('--------------------------------------')
    c2g.print_event_dictionary(event_dict)
    entire_event_dict.update(event_dict)

print('--------------------------------------')
c2g.print_event_dictionary(entire_event_dict)

print('--------------------------------------')

events = []
sets = []
for e, s in entire_event_dict.items():
    events.append(e)
    sets.append(s)

events.reverse()
sets.reverse()

# events as TUPLES
# print(events)

events = c2g.convert_list_of_tuples_to_list_of_sets(events)

name_of_events = c2g.give_names_to_events(events)
print('Names: ' + str(name_of_events))
# events as SETS
print('Events: ' + str(events))
print('Sets: ' + str(sets))
print('--------------------------------------')
print('Children:')
children_ = c2g.find_children_indices(0, events)
print(children_)
print(c2g.find_relationship(0, children_, sets))
print('--------------------------------------')
# print(c2g.is_children_mutual_exclusive_union_of_parent({0, 1, 2, 3}, [{0, 2}, {1, 3}]))
# print(c2g.is_children_identical_to_parent({0, 1, 2, 3}, [{0, 1, 2, 3}, {0, 1, 2, 3}]))
# print(c2g.get_sets_of_indices([4, 2, 3], events))

print(name_of_events[0])
for i in range(len(events)):
    if len(events[i]) > 1:
        children = c2g.find_children_indices(i, events)
        gate = c2g.find_relationship(i, children, sets)
        print(str(gate) + '   parent: ' + str(name_of_events[i]))
        for child in children:
            print(str(name_of_events[child]) + '   parent: ' + str(gate))
