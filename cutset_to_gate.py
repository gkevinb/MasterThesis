from numbers import Number
import collections


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


def give_names_to_event(events):
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
