import collections


is_EVEN = lambda i: i % 2 == 0
is_ODD = lambda i: i % 2 == 1


'''
Gets the index of the number that is right before the number passed in as
an argument in the method.
Arguments:
queue - list of numbers
number - number to find the index of its lower neighbor, so the index of
    the number before number
Returns - the index of the previous number
Ex: queue = [2, 4, 6]
    number = 5
    Returns = 1
'''


def get_index_of_number_before(queue, number):
    # For Testing: #event_time_series = [2, 4, 6]
    index = -1
    # First checks if number is smaller then the first number in series
    if number < queue[0]:
        # print('FIRST')
        index = -1
    # Second checks if number is greater then the last number in series
    elif number > queue[-1]:
        # print('LAST')
        index = len(queue) - 1
    # Then checks the rest of the numbers
    else:
        # print('MIDDLE')
        for i in range(len(queue)):
            if number < queue[i]:
                index = i - 1
                break
    return index


'''
Get the state of the event at a certain time. Basically just means
if the index is odd then the state of the event is UP and if the
index is even then the state is DOWN.

'''


def get_state_of_event(queue, time):
    index = get_index_of_number_before(queue, time)
    if is_ODD(index):
        return 'UP'
    else:
        return 'DOWN'


'''
Get the state of all the basic event at a certain time, basically just
puts the get_state_of_event method into a for loop to find it for all
basic events.
Returns - a list indicating what events were UP or DOWN
'''


def get_state_of_basic_events(basic_events, time):
    status_of_events = []
    for i in range(len(basic_events)):
        basic_event = basic_events[i]
        status_of_events.append(get_state_of_event(basic_event, time))
    return status_of_events


def get_all_cut_sets(top_event, basic_events):
    all_cut_sets = {}
    for i in range(len(top_event)):
        if is_EVEN(i):
            failure = top_event[i]
            all_cut_sets[failure] = get_state_of_basic_events(basic_events, failure)
    all_cut_sets = collections.OrderedDict(sorted(all_cut_sets.items()))
    return all_cut_sets


def calculate_unique_cut_sets(all_cut_sets):
    unique_cut_sets = []
    for time, cut_set in all_cut_sets.items():
        if cut_set not in unique_cut_sets:
            unique_cut_sets.append(cut_set)
    return unique_cut_sets


def convert_cut_set(symbol_cut_set):
    cut_set = []
    for i in range(len(symbol_cut_set)):
        if symbol_cut_set[i] == 'DOWN':
            cut_set.append(i + 1)
    return cut_set


def convert_cut_sets(top_event, basic_events):
    cut_sets = []
    all_cut_sets = get_all_cut_sets(top_event, basic_events)
    symbol_cut_sets = calculate_unique_cut_sets(all_cut_sets)
    for symbol_cut_set in symbol_cut_sets:
        cut_sets.append(convert_cut_set(symbol_cut_set))
    # print('Cut sets: ' + str(cut_sets))
    return cut_sets


'''
cut_set_ut (cut set under test)
'''


def is_reducible_cut_set(cut_set, cut_set_ut):
    counter = 0
    for component in cut_set:
        if component in cut_set_ut:
            counter += 1
    if counter == len(cut_set):
        return True
    else:
        return False


'''
cut_set_op (cut set operator)
'''


def calculate_minimal_cut_sets(cut_sets):
    cut_sets_for_removal = []
    # Get cut_set from cut_sets
    for cut_set in cut_sets:
        # Get another cut_set(_op) from cut_sets
        for cut_set_op in cut_sets:
            # Check if the two cut_set are not the same
            if cut_set != cut_set_op:
                # Check if cut_set_op can be reduced to cut_set
                if is_reducible_cut_set(cut_set, cut_set_op):
                    # If can be reduced set up for removal
                    # Check if cut_set_op is not marked for removal yet
                    if cut_set_op not in cut_sets_for_removal:
                        # If not marked for removal yet, added it for removal
                        cut_sets_for_removal.append(cut_set_op)
    # print(cut_sets_for_removal)
    # Remove the cut_set from cut_sets that are marked for removal
    for cut_set in cut_sets_for_removal:
        cut_sets.remove(cut_set)
    return cut_sets
