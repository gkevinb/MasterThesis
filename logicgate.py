from numbers import Number
import collections

'''
Get a three element list, showing if the transition of the time is from up to down or down to up.
The first element is the edge before the time transition, the second element is the time transition,
the third element is the edge after the time transition. Function finds index of of the time, and if
it's in an even index its U then D, if odd index its D then U
Ex: ['U', 1.5, 'D']
'''


def get_subsequent_edge_type(data_stream, time):
    edges = []
    index = 0
    for i in range(len(data_stream)):
        if data_stream[i] == time:
            index = i
            break
    if index % 2 == 0:
        edges.append('U')
        edges.append(time)
        edges.append('D')
    else:
        edges.append('D')
        edges.append(time)
        edges.append('U')
    return edges


'''
Create a sorted dictionary of all the transition times in all the data streams. The keys are the 
transition times because these will be unique, the values are the index of which data stream it
belongs to.
'''


def create_data_stream_dict(a_data_streams):
    data_dict = {}
    for i in range(len(a_data_streams)):
        length = len(a_data_streams[i])
        stream = a_data_streams[i]
        for j in range(length):
            data_dict[stream[j]] = i
    ordered_dict = collections.OrderedDict(sorted(data_dict.items()))
    return ordered_dict


'''
Create empty data_streams which hold enough space for all the transition times plus the
corresponding edge transitions.
'''


def initialize_coded_data_streams(size, num_of_streams):
    coded_data_streams = []
    for i in range(num_of_streams):
        i_coded_data_stream = [None] * (size * 2 + 1)
        i_coded_data_stream[0] = 'U'
        coded_data_streams.append(i_coded_data_stream)
    return coded_data_streams


'''
Initialize empty data stream to save result
'''


def initialize_result_data_stream(size):
    empty_list = [None] * (size * 2 + 1)
    return empty_list


'''
Fill out missing entries in edge_transition_coded_data_streams by looking at previous element.
'''


def fill_out_missing_entries(coded_data_streams):
    for i in range(len(coded_data_streams)):
        i_coded_data_stream = coded_data_streams[i]
        length = len(i_coded_data_stream)
        for j in range(length):
            if i_coded_data_stream[j] is None:
                i_coded_data_stream[j] = i_coded_data_stream[j - 1]


'''
Function to check if all elements in the slice are UP
'''


def is_all_up(slice_):
    decision = False
    i = 0
    for element in slice_:
        if element == 'U':
            i += 1
    if i == len(slice_):
        decision = True
    return decision


'''
Function to check if all elements in the slice are UP
'''


def is_all_down(slice_):
    decision = False
    i = 0
    for element in slice_:
        if element == 'D':
            i += 1
    if i == len(slice_):
        decision = True
    return decision


'''
Function to check if at least one element is a number, meaning there is a transition there
'''


def is_number_in_slice(slice_):
    decision = False
    for element in slice_:
        if isinstance(element, Number):
            decision = True
            break
    return decision


'''
Function to get number, the transition time, in that slice.
'''


def get_number_in_slice(slice_):
    number = 0
    for element in slice_:
        if isinstance(element, Number):
            number = element
            break
    return number


'''
Evaluate slice according to AND gate
'''


def and_evaluate_slice(slice_):
    if is_all_up(slice_):
        element = 'U'
    elif is_number_in_slice(slice_):
        element = get_number_in_slice(slice_)
    else:
        element = 'D'
    return element


'''
Evaluate slice according to AND gate
'''


def or_evaluate_slice(slice_):
    if is_all_down(slice_):
        element = 'D'
    elif is_number_in_slice(slice_):
        element = get_number_in_slice(slice_)
    else:
        element = 'U'
    return element


'''
Evaluate edge_transition_coded_data_streams by taking each index at a time and creating a 'slice'
from the streams that happen at the same instant. 
i is the index of the stream, j is the index of the slice
'''


def evaluate_transitions(gate, coded_data_streams, length):
    result_list = initialize_result_data_stream(length)
    for i in range(len(coded_data_streams[0])):
        slice_ = []
        for j in range(len(coded_data_streams)):
            slice_.append(coded_data_streams[j][i])
            if gate == 'AND':
                result_list[i] = and_evaluate_slice(slice_)
            if gate == 'OR':
                result_list[i] = or_evaluate_slice(slice_)
    return result_list


'''
Filter out the UP and DOWN elements from data stream just to get transition times
'''


def filter_stream(stream):
    result_list = []
    for i in range(len(stream)):
        if isinstance(stream[i], Number):
            if stream[i - 1] != stream[i + 1]:
                result_list.append(stream[i])
    return result_list


'''
Evaluate the streams according to the gate, gate can be 'AND' or 'OR'
Returns a data stream containing the edge transition times after the 
logic gate.
'''


def evaluate(gate, streams):
    sorted_stream = create_data_stream_dict(streams)

    edge_transition_coded_data_streams = initialize_coded_data_streams(len(sorted_stream), len(streams))

    '''
    Fill out edge_transition_coded_data_streams according to the transition times in
    increasing order. While keeping space between entries if another stream has entries
    in those spots.
    '''
    counter = 0
    for key, value in sorted_stream.items():
        edge = get_subsequent_edge_type(streams[value], key)
        i_coded_data_stream = edge_transition_coded_data_streams[value]
        i_coded_data_stream[counter] = edge[0]
        counter += 1
        i_coded_data_stream[counter] = edge[1]
        counter += 1
        i_coded_data_stream[counter] = edge[2]

    fill_out_missing_entries(edge_transition_coded_data_streams)

    result = evaluate_transitions(gate, edge_transition_coded_data_streams, len(sorted_stream))

    result = filter_stream(result)

    return result
