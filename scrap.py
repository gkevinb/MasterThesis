from numbers import Number

print(isinstance('4.45', Number))

print(6 % 2)


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


print(get_subsequent_edge_type([2, 3, 4, 5], 3))

l = [[1,2,3], [4,5,6], [7,8,9]]
print(l[1][2])


'''
counter = 0
for key, value in sorted_stream.items():
    if value == 'x':
        edge = get_subsequent_edge_type(x, key)
        x_list[counter] = edge[0]
        counter += 1
        x_list[counter] = edge[1]
        counter += 1
        x_list[counter] = edge[2]

    if value == 'y':
        edge = get_subsequent_edge_type(y, key)
        y_list[counter] = edge[0]
        counter += 1
        y_list[counter] = edge[1]
        counter += 1
        y_list[counter] = edge[2]

'''