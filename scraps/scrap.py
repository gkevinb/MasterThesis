import itertools

mylist = range(5)


p = {0, 1, 2}
children = [{0, 1}, {0, 2}, {1, 2}]
for x, y in itertools.combinations(children, 2):
    print(x, y)

print('----------------------------------')
for x in children:
    # Get another cut_set(_under_test) from cut_sets
    for y in children:
        # Check if the two cut_set are not the same
        if x != y:
            print(x, y)
