from numbers import Number
import collections


EMPTY_LIST = list()


def get_basic_events(cut_sets):
    basic_events = set()
    for cut_set in cut_sets:
        for event in cut_set:
            basic_events.add(event)
        '''
        # PROBABLY UNNEEDED IF CUT SETS ARE ENTERED LIKE THIS cut_sets = ((1, 2),) AND NOT LIKE THIS cut_sets = (1, 2) 
        if isinstance(cut_set, Number):
            basic_events.add(cut_set)
        else:
            for event in cut_set:
                basic_events.add(event)
        '''

    return basic_events


def create_event_cut_set_dict(basic_events, cut_sets):
    event_dictionary = {}

    for basic_event in basic_events:
        event = [basic_event]
        cut_set_ids = set()
        for i in range(len(cut_sets)):
            if basic_event in cut_sets[i]:
                cut_set_ids.add(i)
        event_dictionary[tuple(event)] = cut_set_ids

    return event_dictionary


def is_sets_identical(set1, set2):
    if set1 == set2:
        return True
    else:
        return False


def is_sets_mutually_exclusive(set1, set2):
    if set1.isdisjoint(set2):
        return True
    else:
        return False


def print_event_dictionary(event_dictionary):
    for event, sets in event_dictionary.items():
        print('Event: ' + str(event) + ' - Sets: ' + str(sets))


def add_to_event_set(event_set, event):
    for e in event:
        event_set.add(e)


def find_identical_sets(event_dictionary):
    identical_sets = {}
    for event, sets in event_dictionary.items():
        event_set = set()
        add_to_event_set(event_set, event)
        for event_op, sets_op in event_dictionary.items():
            if event is not event_op:
                if is_sets_identical(sets, sets_op):
                    add_to_event_set(event_set, event_op)
        identical_sets[tuple(event_set)] = sets
    return identical_sets


def find_mutual_exclusive_sets(event_dictionary):
    mutual_exclusive_sets = {}
    for event, sets in event_dictionary.items():
        event_set = set()
        add_to_event_set(event_set, event)
        for event_op, sets_op in event_dictionary.items():
            if event is not event_op:
                if is_sets_mutually_exclusive(sets, sets_op):
                    add_to_event_set(event_set, event_op)
                    sets = sets.union(sets_op)
        mutual_exclusive_sets[tuple(event_set)] = sets
    return mutual_exclusive_sets


def give_names_to_events(events):
    length = len(events)
    names = ['NULL'] * length

    # Top Event
    names[0] = 'Top Event'
    basic_event_index = 1

    for i in range(1, length):
        if len(events[i]) > 1:
            intermediate_event_name = 'Intermediate Event ' + str(i)
            names[i] = intermediate_event_name
        if len(events[i]) == 1:
            basic_event_name = 'Basic Event ' + str(basic_event_index)
            names[i] = basic_event_name
            basic_event_index += 1

    return names


def convert_list_of_tuples_to_list_of_sets(list_of_tuples):
    list_of_sets = []
    for tuple_ in list_of_tuples:
        set_ = set(tuple_)
        list_of_sets.append(set_)
    return list_of_sets


def reverse_events_and_sets(events, sets):
    top_event_length = len(events[-1])
    grouped_events = []
    grouped_sets = []
    for i in range(1, top_event_length + 1):
        i_event_group = []
        i_set_group = []
        for j in range(len(events)):
            if len(events[j]) == i:
                i_event_group.append(events[j])
                i_set_group.append(sets[j])

        grouped_events.append(i_event_group)
        grouped_sets.append(i_set_group)

    grouped_events.reverse()
    grouped_sets.reverse()

    events = []
    sets = []

    for i in range(len(grouped_events)):
        if grouped_events[i] != EMPTY_LIST:
            for event_ in grouped_events[i]:
                events.append(event_)
        if grouped_events[i] != EMPTY_LIST:
            for set_ in grouped_sets[i]:
                sets.append(set_)

    return events, sets


def find_children_indices(parent_index, events):
    parent = events[parent_index]
    children = []
    sub_events = set()
    for i in range(len(events)):
        if parent is not events[i]:
            if events[i].issubset(parent):
                sub_events.update(events[i])
                children.append(i)
            if is_sets_identical(sub_events, parent):
                break
    return children


def get_sets_of_indices(indices, sets):
    list_of_sets = []
    for index in indices:
        list_of_sets.append(sets[index])
    return list_of_sets


def is_children_identical_to_parent(parent, children):
    decision = False
    counter = 0
    for child in children:
        if is_sets_identical(child, parent):
            counter += 1

    if counter == len(children):
        decision = True

    return decision


# NOT USED, PROBABLY NOT NEEDED
def n_choose_2(n):
    if n > 1:
        return (n * (n - 1))/2
    else:
        return 0


def is_children_mutual_exclusive_union_of_parent(parent, children):
    sets = set()
    decision = False
    tick = True
    for child in children:
        for child_ in children:
            if child is not child_:
                if is_sets_mutually_exclusive(child, child_):
                    pass
                else:
                    tick = False
    if tick:
        for child in children:
            sets.update(child)
        if is_sets_identical(sets, parent):
            decision = True

    return decision


def find_relationship(parent_index, children_indices, sets):
    parent = sets[parent_index]
    children = get_sets_of_indices(children_indices, sets)
    relationship = 'NULL'

    if is_children_identical_to_parent(parent, children):
        relationship = 'AND'
    if is_children_mutual_exclusive_union_of_parent(parent, children):
        relationship = 'OR'

    return relationship


def get_object_name(name):
    return name.lower().replace(' ', '_')


def get_object_names(names):
    object_names = []
    for name in names:
        object_names.append(get_object_name(name))
    return object_names
