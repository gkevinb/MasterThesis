from numbers import Number


x = [3, 5, 7, 9]
y = [2, 4, 8]
z = [1, 6, 10]
data_streams = [x, y, z]
print(x)
print(y)
print(z)



'''
Get a three element list, showing if the transition of the time is from up to down or down to up.
The first element is the edge before the time transition, the second element is the time transition,
the third element is the edge after the time transition. Function finds index of of the time, and if
it's in an even index its U then D, if odd index its D then U
Ex: ['U', 1.5, 'D']
'''
def get_subsequent_edge_type(data_stream, time):
    edges = []
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
def create_datastream_dict(a_data_streams):
    data_dict = {}
    for i in range(len(a_data_streams)):
        length = len(a_data_streams[i])
        stream = a_data_streams[i]
        for j in range(length):
            data_dict[stream[j]] = i
    return data_dict


sorted_stream = create_datastream_dict(data_streams)
print(sorted_stream)



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


edge_transition_coded_data_streams = initialize_coded_data_streams(len(sorted_stream), len(data_streams))

'''
Initialize empty data stream to save result
'''
def initialize_result_data_stream(size):
    empty_list = [None] * (size * 2 + 1)
    return empty_list



print(edge_transition_coded_data_streams)

'''
Fill out edge_transition_coded_data_streams according to the transition times in
increasing order. While keeping space between entries if another stream has entries
in those spots.
'''
counter = 0
for key, value in sorted_stream.items():
    edge = get_subsequent_edge_type(data_streams[value], key)
    i_coded_data_stream = edge_transition_coded_data_streams[value]
    i_coded_data_stream[counter] = edge[0]
    counter += 1
    i_coded_data_stream[counter] = edge[1]
    counter += 1
    i_coded_data_stream[counter] = edge[2]


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


fill_out_missing_entries(edge_transition_coded_data_streams)

print(edge_transition_coded_data_streams)


'''
Function to check if all elements in the slice are UP
'''
def is_all_up(slice):
    decision = False
    i = 0
    for element in slice:
        if element == 'U':
            i += 1
    if i == len(slice):
        decision = True
    return decision


'''
Function to check if all elements in the slice are UP
'''
def is_all_down(slice):
    decision = False
    i = 0
    for element in slice:
        if element == 'D':
            i += 1
    if i == len(slice):
        decision = True
    return decision


'''
Function to check if at least one element is a number, meaning there is a transition there
'''
def is_number_in_slice(slice):
    decision = False
    for element in slice:
        if isinstance(element, Number):
            decision = True
            break
    return decision

'''
Function to get number, the transition time, in that slice.
'''
def get_number_in_slice(slice):
    number = 0
    for element in slice:
        if isinstance(element, Number):
            number = element
            break
    return number


'''
Evaluate slice according to AND gate
'''
def and_evaluate_slice(slice):
    if is_all_up(slice):
        element = 'U'
    elif is_number_in_slice(slice):
        element = get_number_in_slice(slice)
    else:
        element = 'D'
    return element

'''
Evaluate slice according to AND gate
'''
def or_evaluate_slice(slice):
    if is_all_down(slice):
        element = 'D'
    elif is_number_in_slice(slice):
        element = get_number_in_slice(slice)
    else:
        element = 'U'
    return element


'''
Evaluate edge_transition_coded_data_streams by taking each index at a time and creating a 'slice'
from the streams that happen at the same instant. 
i is the index of the stream, j is the index of the slice
'''
def evaluate(coded_data_streams, gate):
    result_list = initialize_result_data_stream(len(sorted_stream))
    for i in range(len(coded_data_streams[0])):
        slice = []
        for j in range(len(coded_data_streams)):
            slice.append(coded_data_streams[j][i])
            if gate == 'AND':
                result_list[i] = and_evaluate_slice(slice)
            if gate == 'OR':
                result_list[i] = or_evaluate_slice(slice)
    return result_list


result = evaluate(edge_transition_coded_data_streams, 'AND')


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

and_result = filter_stream(result)
print(and_result)