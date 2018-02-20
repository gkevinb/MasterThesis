from numbers import Number


x = [3, 5, 7, 9]
y = [2, 4, 8]
z = [1, 6, 10]

print(x)
print(y)


'''
DataStream class not needed
'''
class DataStream:
    def __init__(self, stream, name):
        self.stream = stream
        self.name = name
        self.place = 0
        self.top = True
        self.length = len(stream)

    def step(self):
        self.place += 1
        if self.top:
            self.top = False
        else:
            self.top = True

    def get_edge(self):
        return self.top

    def current(self):
        return self.stream[self.place]

    def __repr__(self):
        return str(self.stream[self.place]) + ' : ' + str(self.top)


# Not needed

x1 = DataStream(x, 'x')
y1 = DataStream(y, 'y')


# Not needed
def append_edges(data_stream):
    data = ['U']
    for i in range(data_stream.length):
        data.append(data_stream.current())
        data_stream.step()
        if data_stream.get_edge():
            data.append('U')
        else:
            data.append('D')
    return data


def get_subsequent_edge_type(data_stream, time):
    edges = []
    for j in range(len(data_stream)):
        if data_stream[j] == time:
            index = j
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


# Not needed
d_1 = append_edges(x1)
d_2 = append_edges(y1)


data_streams = [x, y, z]
print(d_1)
print(d_2)


def create_data_dict(data):
    data_dict = {}
    for _i in range(len(data)):
        for k in range((len(data[_i]))):
            stream = data[_i]
            data_dict[stream[k]] = _i
    return data_dict


sorted_stream = create_data_dict(data_streams)
print(sorted_stream)

coded_list = []
for i in range(len(data_streams)):
    i_list = [None] * (len(sorted_stream) * 2 + 1)
    i_list[0] = 'U'
    coded_list.append(i_list)

'''
x_list = [None] * (len(sorted_stream) * 2 + 1)
y_list = [None] * (len(sorted_stream) * 2 + 1)
and_list = [None] * (len(sorted_stream) * 2 + 1)
x_list[0] = 'U'
y_list[0] = 'U'
print(x_list)
print(y_list)
'''
and_list = [None] * (len(sorted_stream) * 2 + 1)
print(coded_list)


counter = 0
for key, value in sorted_stream.items():
    edge = get_subsequent_edge_type(data_streams[value], key)
    j_list = coded_list[value]
    j_list[counter] = edge[0]
    counter += 1
    j_list[counter] = edge[1]
    counter += 1
    j_list[counter] = edge[2]

for i in range(len(coded_list)):
    j_list = coded_list[i]
    for j in range(len(j_list)):
        if j_list[j] is None:
            j_list[j] = j_list[j - 1]

print(coded_list)
'''
for i in range(len(x_list)):
    if x_list[i] is None:
        x_list[i] = x_list[i - 1]
    if y_list[i] is None:
        y_list[i] = y_list[i - 1]
print(x_list)
print(y_list)
'''


def is_all_up(_slice):
    decision = False
    _counter = 0
    for sl in _slice:
        if sl == 'U':
            _counter += 1
    if _counter == len(_slice):
        decision = True
    return decision


def is_number_in_it(_slice):
    decision = False
    for sl in _slice:
        if isinstance(sl, Number):
            decision = True
            break
    return decision


def get_number_in_it(_slice):
    num = 0
    for sl in _slice:
        if isinstance(sl, Number):
            num = sl
            break
    return num


def evaluate_slice(_slice):
    if is_all_up(_slice):
        _s = 'U'
    elif is_number_in_it(_slice):
        _s = get_number_in_it(_slice)
    else:
        _s = 'D'
    return _s


for i in range(len(coded_list[0])):
    sli = []
    for j in range(len(coded_list)):
        sli.append(coded_list[j][i])
    and_list[i] = evaluate_slice(sli)

print(and_list)

and_result = []

for i in range(len(and_list)):
    if isinstance(and_list[i], Number):
        if and_list[i - 1] != and_list[i + 1]:
            and_result.append(and_list[i])

print(and_result)
