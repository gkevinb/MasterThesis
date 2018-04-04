from numbers import Number


EMPTY_LIST = list()


def get_basic_events(minimal_cut_sets):
    """
    Get list of basic events from the list of minimal cut sets.
    :param minimal_cut_sets: List of minimal cut sets
    :return: List of basic events
    """
    basic_events = set()
    for cut_set in minimal_cut_sets:
        for event in cut_set:
            basic_events.add(event)

    return basic_events


def create_event_cut_set_dict(basic_events, minimal_cut_sets):
    """
    Create a dictionary where the keys are index of basic events (index starts from 1) and the value is the
    indices of the minimal cut sets (index starts from 0) which include that basic event.
    :param basic_events: Set which includes the index of basic events (index starts from 1)
    :param minimal_cut_sets: List of minimal cut sets (index starts from 0)
    :return: Returns event dictionary
    """
    event_dictionary = {}

    for basic_event in basic_events:
        minimal_cut_set_ids = set()
        for i in range(len(minimal_cut_sets)):
            if basic_event in minimal_cut_sets[i]:
                minimal_cut_set_ids.add(i)
        event_dictionary[tuple([basic_event])] = minimal_cut_set_ids

    return event_dictionary


def is_sets_identical(set1, set2):
    """
    Checks if the two sets are identical or not.
    :param set1: First set
    :param set2: Second set
    :return: True if sets are identical, False if not
    """
    if set1 == set2:
        return True
    else:
        return False


def is_sets_mutually_exclusive(set1, set2):
    """
    Checks if the two sets are mutually exclusive or not.
    :param set1: First set
    :param set2: Second set
    :return: True if sets are mutually exclusive, False if not
    """
    if set1.isdisjoint(set2):
        return True
    else:
        return False


def print_event_dictionary(event_dictionary):
    """
    Print the event dictionary in easily readable format.
    :param event_dictionary: Event dictionary
    :return:
    """
    for event, sets in event_dictionary.items():
        print('Event: ' + str(event) + ' - Sets: ' + str(sets))


def add_to_event_set(event_set, event):
    """
    Add event to a set of events
    :param event_set: Set of events
    :param event: An event
    :return:
    """
    for e in event:
        event_set.add(e)


# COMBINE TWO METHODS BELOW INTO ONE
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


def find_interconnected_sets(event_dictionary):
    interconnected_sets = {}
    for event, sets in event_dictionary.items():
        event_set = set()
        add_to_event_set(event_set, event)
        for event_op, sets_op in event_dictionary.items():
            if event is not event_op:
                if not is_sets_identical(sets, sets_op) and not is_sets_mutually_exclusive(sets, sets_op):
                    add_to_event_set(event_set, event_op)
                    sets = sets.union(sets_op)
        interconnected_sets[tuple(event_set)] = sets
    return interconnected_sets


def expand_event_dictionary(event_dictionary):
    entire_event_dictionary = {}
    entire_event_dictionary.update(event_dictionary)

    print('--------------------------------------')
    print_event_dictionary(event_dictionary)
    # ALGORITHM STILL NEEDS TO BE OPTIMIZED!!!!!!!!
    while len(event_dictionary) != 1:
        event_dictionary = find_identical_sets(event_dictionary)
        print('--------------------------------------')
        print_event_dictionary(event_dictionary)
        entire_event_dictionary.update(event_dictionary)

        # K/N VOTING SHOULD PROBABLY GO RIGHT HERE!!!!!!!!!
        event_dictionary = find_interconnected_sets(event_dictionary)
        print('--------------------------------------')
        print_event_dictionary(event_dictionary)
        entire_event_dictionary.update(event_dictionary)

        event_dictionary = find_mutual_exclusive_sets(event_dictionary)
        print('--------------------------------------')
        print_event_dictionary(event_dictionary)
        entire_event_dictionary.update(event_dictionary)

    print('--------------------------------------')
    print_event_dictionary(entire_event_dictionary)

    print('--------------------------------------')
    return entire_event_dictionary


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
    # print('Events: ' + str(events))
    parent = events[parent_index]
    # print('parent: ' + str(parent))
    children = []
    sub_events = set()

    for i in range(len(events)):
        if parent is not events[i]:
            if events[i].issubset(parent):
                # If children already a subset of sub_events, don't add them again
                if not events[i].issubset(sub_events):
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


def is_children_n_choose_k(parent, children):
    decision = True

    for child in children:
        for child_ in children:
            if child is not child_:
                if is_sets_identical(child, child_):
                    decision = False
                if is_sets_mutually_exclusive(child, child_):
                    decision = False
                if not child.intersection(child_):
                    decision = False
                if not child.issubset(parent):
                    decision = False
                if len(child) != len(child_):
                    decision = False

    return decision


def get_n_in_voting_gate(parent, children):
    n = len(parent)
    n_simplified = len(children)
    k = len(children[0])
    # print('N = ' + str(n))
    # print('N simplified = ' + str(n_simplified))
    # print('k = ' + str(k))

    k_simplified = int(k / (n / n_simplified))
    # print('k simplified: ' + str(k_simplified))
    return k_simplified


def find_relationship(parent_index, children_indices, sets):
    parent = sets[parent_index]
    children = get_sets_of_indices(children_indices, sets)
    relationship = 'NULL'
    # print('Children: ' + str(children))
    # print('Parent: ' + str(parent))

    if is_children_identical_to_parent(parent, children):
        relationship = 'AND'
    if is_children_mutual_exclusive_union_of_parent(parent, children):
        relationship = 'OR'
    if is_children_n_choose_k(parent, children):
        relationship = get_n_in_voting_gate(parent, children)

    return relationship


def get_object_name(name):
    """
    Converts the name string by replacing ' ' (space) with '_' (underscore) and changing the letters to lowercase.
    :param name: A string
    :return: Converted string
    """
    return name.lower().replace(' ', '_')


def get_object_names(names):
    """
    Calls the get_object_name method in a loop for each name in the list of names.
    :param names: List of strings
    :return: List of converted strings
    """
    object_names = []
    for name in names:
        object_names.append(get_object_name(name))
    return object_names


def print_out_fault_tree(event_dictionary):

    events, sets = zip(*event_dictionary.items())

    events, sets = reverse_events_and_sets(events, sets)

    events = convert_list_of_tuples_to_list_of_sets(events)

    name_of_events = give_names_to_events(events)
    object_event_names = get_object_names(name_of_events)

    print('--------------------------------------')
    print(str(object_event_names[0]) + ' = Event("' + name_of_events[0] + '")')
    for i in range(len(events)):
        if len(events[i]) > 1:
            children = find_children_indices(i, events)
            gate = find_relationship(i, children, sets)
            k = 0
            # print('Gate: ' + gate)
            if isinstance(gate, Number):
                k = gate
                gate = 'VOTING'
            object_gate = get_object_name(gate) + str(i + 1)
            print(str(object_gate) + ' = Gate("' + str(gate) + '", parent=' + str(object_event_names[i]),
                  end="", flush=True)
            if k > 0:
                print(', k=' + str(k) + ')')
            else:
                print(')')
            for j in range(len(children)):
                child = children[j]
                print(str(object_event_names[child]) + ' = Event("' + str(name_of_events[child]) +
                      '", parent=' + str(object_gate) + ')')

    print('--------------------------------------')


def reconstruct_fault_tree(minimal_cut_sets):
    basic_events = get_basic_events(minimal_cut_sets)

    event_dict = create_event_cut_set_dict(basic_events, minimal_cut_sets)

    entire_event_dict = expand_event_dictionary(event_dict)

    print_out_fault_tree(entire_event_dict)
