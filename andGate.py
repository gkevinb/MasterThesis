from numbers import Number


x = [1, 3, 5]
y = [2, 4]

print(x)
print(y)


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


x1 = DataStream(x, 'x')
y1 = DataStream(y, 'y')


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


d_1 = append_edges(x1)
d_2 = append_edges(y1)
data_streams = [x1, y1]
print(d_1)
print(d_2)


def make_dictionary(data):
    a_dict = {}
    for d in data:
        for i in range(d.length):
            a_dict[d.stream[i]] = d.name
    return a_dict


sorted_stream = make_dictionary(data_streams)
print(sorted_stream)
x_list = [None] * (len(sorted_stream) * 2 + 1)
y_list = [None] * (len(sorted_stream) * 2 + 1)
and_list = [None] * (len(sorted_stream) * 2 + 1)
x_list[0] = 'U'
y_list[0] = 'U'
print(x_list)
print(y_list)

counter = 0
for key, value in sorted_stream.items():
    #print(str(key) + ' ' + value)
    if value == 'x':
        for i in range(len(d_1)):
            if d_1[i] == key:
                x_list[counter] = d_1[i - 1]
                counter += 1
                x_list[counter] = d_1[i]
                counter += 1
                x_list[counter] = d_1[i + 1]
                #counter += 1
    if value == 'y':
        for i in range(len(d_2)):
            if d_2[i] == key:
                y_list[counter] = d_2[i - 1]
                counter += 1
                y_list[counter] = d_2[i]
                counter += 1
                y_list[counter] = d_2[i + 1]
                #counter += 1

for i in range(len(x_list)):
    if x_list[i] is None:
        x_list[i] = x_list[i - 1]
    if y_list[i] is None:
        y_list[i] = y_list[i - 1]
print(x_list)
print(y_list)


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


for i in range(len(x_list)):
    s = [x_list[i], y_list[i]]
    and_list[i] = evaluate_slice(s)

print(and_list)

and_result = []

for i in range(len(and_list)):
    if isinstance(and_list[i], Number):
        if and_list[i - 1] != and_list[i + 1]:
            and_result.append(and_list[i])

print(and_result)