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

events = []
sets = []
for e, s in entire_event_dict.items():
    events.append(e)
    sets.append(s)

events.reverse()
sets.reverse()

print(events)
print(sets)

print(c2g.give_names_to_event(events))
