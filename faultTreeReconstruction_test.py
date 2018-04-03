import faultTreeReconstruction as ftr


# cut_sets = [[1, 2], [3, 4]]
cut_sets = [[1, 3], [1, 4], [2, 3], [2, 4]]
# cut_sets = ((1,), (2,))
# cut_sets = ((1, 2), (3,), (4,))
# CANT HANDLE # cut_sets = (1, 2) BECAUSE IT IS ONLY ONE CUT SET,
# SO WRITE THIS INSTEAD:
# cut_sets = ((1, 2),)
# cut_sets = [[1, 2, 3], [1, 2, 4]]


basic_events = ftr.get_basic_events(cut_sets)

event_dict = ftr.create_event_cut_set_dict(basic_events, cut_sets)

entire_event_dict = ftr.expand_event_dictionary(event_dict)

ftr.reconstruct_fault_tree(entire_event_dict)


# --------------------------- USE CODE BELOW TO WRITE UNIT TESTS --------------------------------- #


'''
print('Names: ' + str(name_of_events))
# events as SETS
print('Events: ' + str(events))
print('Sets: ' + str(sets))
print('--------------------------------------')
print('Children:')
children_ = ftr.find_children_indices(0, events)
print(children_)
print(ftr.find_relationship(0, children_, sets))
print('--------------------------------------')
'''

# print(c2g.is_children_mutual_exclusive_union_of_parent({0, 1, 2, 3}, [{0, 2}, {1, 3}]))
# print(c2g.is_children_identical_to_parent({0, 1, 2, 3}, [{0, 1, 2, 3}, {0, 1, 2, 3}]))
# print(c2g.get_sets_of_indices([4, 2, 3], events))
